"""``manage.py seed`` — build the whole encyclopedia from the corpus.

What this command guarantees, and why each guarantee exists:

**It validates before it writes.** The corpus is checked by
:func:`validators.validate_corpus` and a single problem aborts the run with
nothing written. A half-seeded encyclopedia is harder to diagnose than an empty
one.

**It refuses to overwrite pre-cutover content.** An article whose slug is in the
corpus but whose history this seed did not write belongs to the old deployment
(DECISIONS §8). The command stops and prints the exact recovery command rather
than silently rewriting somebody's article. ``--flush --force`` is the way to say
"yes, wipe it".

**It is deterministic.** Every synthesised value — how many revisions an article
has, when they were made, who made them, its view count, which articles have talk
threads — comes from a BLAKE2b hash of the article title, never from
:func:`datetime.now` and never from an unseeded :mod:`random`. Re-running the
command produces byte-identical rows, and the printed counts are therefore a real
idempotency test.

**It produces the apparatus, not just the prose.** References, redirects from
aliases, ``ArticleLink`` rows *including the unresolved ones* that make red links
and "what links here" work, main-page blocks, talk threads, watches and view
counts. A feature with no data looks broken, so every feature gets data.

Synthesised history is built by *growing* the article: revision 1 holds the lead
and the first sections, each later revision adds more blocks, and the last holds
exactly the published text. That makes ``/api/articles/{slug}/diff/`` show real
added paragraphs and ``byte_delta`` real numbers, which a random walk would not.

Usage::

    manage.py seed                     # create or update everything
    manage.py seed --check             # validate the corpus and stop
    manage.py seed --rules             # print the corpus contract and stop
    manage.py seed --only zero --only entropy
    manage.py seed --flush --force     # wipe all content first, then reseed
"""

from __future__ import annotations

import datetime as dt
import hashlib
import random
from dataclasses import dataclass
from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.articles.markup import count_footnotes
from apps.articles.models import (
    Article,
    ArticleLink,
    Category,
    MainPageBlock,
    Redirect,
    Reference,
    Revision,
    TalkMessage,
    TalkThread,
    Watch,
)
from apps.common.utils import RESERVED_SLUGS, wiki_slug

from ._seed_data import ARTICLES
from ._seed_data.meta import (
    CATEGORIES,
    DID_YOU_KNOW,
    FEATURED,
    ON_THIS_DAY,
    REDIRECTS,
)
from .validators import RULES, storage_notes, validate_corpus

User = get_user_model()

# --------------------------------------------------------------------------- #
# Determinism
# --------------------------------------------------------------------------- #
#: The instant every synthesised history ends before. A constant, not
#: ``timezone.now()``: with ``now()`` the same command run twice would write
#: different timestamps and the whole idempotency claim would be false.
EPOCH = dt.datetime(2026, 9, 27, 9, 0, tzinfo=dt.UTC)

#: Domain for contributor accounts. ``.invalid`` is reserved by RFC 2606, so
#: these addresses can never reach a real mailbox however the demo is deployed.
CONTRIBUTOR_DOMAIN = "contributors.wikiverse.invalid"

#: Tag written on every revision this command creates. It is how the pre-cutover
#: guard recognises its own work; without it the guard cannot tell a seeded
#: article from a legacy one.
SEED_TAG = "seed"

MIN_REVISIONS = 2
MAX_REVISIONS = 9


def title_seed(title: str) -> int:
    """A stable 64-bit integer derived from ``title``.

    ``hash()`` is salted per process and would make the seed non-reproducible,
    so this uses BLAKE2b, which is fixed for all time.
    """
    digest = hashlib.blake2b(title.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "big")


def rng_for(title: str, purpose: str = "") -> random.Random:
    """A private, reproducible generator for one article and one purpose.

    Separate purposes get separate streams, so adding a talk thread cannot shift
    the revision timestamps of an article that was already seeded.
    """
    return random.Random(title_seed(f"{purpose}\x00{title}"))


# --------------------------------------------------------------------------- #
# The contributor cast
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Contributor:
    username: str
    first_name: str
    last_name: str
    bio: str
    is_bot: bool = False


#: A small, fixed cast. **No superuser** — ``manage.py ensure_admin`` owns that
#: (DECISIONS §8) — and every account is created with an unusable password, so
#: seeding a public demo cannot hand anybody a login.
CAST: tuple[Contributor, ...] = (
    Contributor(
        "hbergmann",
        "Helena",
        "Bergmann",
        "Mathematician by training, copyeditor by temperament. Watches the "
        "mathematics and physics categories and rewrites leads that bury the point.",
    ),
    Contributor(
        "tokonkwo",
        "Tobenna",
        "Okonkwo",
        "Writes about the history of science and about West African trade networks. "
        "Prefers a primary source to a tidy story.",
    ),
    Contributor(
        "mirasvensson",
        "Mira",
        "Svensson",
        "Marine biologist. Adds reef, cephalopod and pollination material, and "
        "chases down the licence on every photograph she uploads.",
    ),
    Contributor(
        "kdesouza",
        "Kalil",
        "de Souza",
        "Geologist. Interested in how quickly a consensus can change once the "
        "evidence is in, which is most of what he writes about.",
    ),
    Contributor(
        "anitraverso",
        "Ana",
        "Traverso",
        "Cartographer and archivist. Fixes place names, coordinates and the "
        "captions nobody else reads.",
    ),
    Contributor(
        "jmorrow",
        "Joss",
        "Morrow",
        "Software engineer. Maintains the reference apparatus and argues about "
        "citation style on talk pages.",
    ),
    Contributor(
        "lfeuerbach",
        "Liesel",
        "Feuerbach",
        "Historian of medicine. Sceptical of origin stories with a single hero in them.",
    ),
    Contributor(
        "wikiverse-bot",
        "Wikiverse",
        "Bot",
        "Automated maintenance account: link repair, reference formatting and "
        "typo sweeps. Flagged 'b' in Recent changes.",
        is_bot=True,
    ),
)

#: Human editors, i.e. the cast minus the bot. Authorship rotates across these.
HUMANS: tuple[Contributor, ...] = tuple(person for person in CAST if not person.is_bot)


# --------------------------------------------------------------------------- #
# Edit summaries
#
# A summary has to match the edit it describes, or the history reads as
# generated: "Bot: removed trailing whitespace" against +1,478 bytes fools
# nobody. So the summary pools are keyed to the *kind* of revision, and the kind
# is chosen before the content is (see :func:`_revision_stages`). POLISH pools
# hold only edits that plausibly change no bytes at all, because that is exactly
# what a polish revision does.
# --------------------------------------------------------------------------- #
CREATION_SUMMARIES = (
    "Created the article",
    "Start of an article on this topic",
    "First draft, lead and opening sections",
    "Created page with lead and outline",
)

GROWTH_SUMMARIES = (
    "Expanded an existing section with sourced detail",
    "Added a paragraph on the mechanism, with a citation",
    "Filled out a section that was only a placeholder",
)

POLISH_SUMMARIES = (
    "Copyedit: removed an editorialising adverb",
    "Fixed a typo",
    "Consistent hyphenation throughout",
    "Reworded a clause that implied more certainty than the source does",
    "Swapped two sentences so the chronology reads forward",
    "Normalised the spelling of a name",
    "Linked the first mention of a related topic instead of the third",
)

BOT_SUMMARIES = (
    "Bot: normalised reference punctuation",
    "Bot: repaired a wikilink to a renamed title",
    "Bot: removed trailing whitespace",
    "Bot: standardised the units in the infobox",
)

#: Kinds a synthesised revision can have. ``create`` is always first and a
#: ``grow`` holding the published text is always last.
CREATE, GROW, POLISH = "create", "grow", "polish"


# --------------------------------------------------------------------------- #
# Talk page material
# --------------------------------------------------------------------------- #
THREAD_TOPICS = (
    ("Lead is too technical", "opener_lead"),
    ("Scope of the “{section}” section", "opener_scope"),
    ("Source for the figure in the infobox", "opener_infobox"),
    ("Should this be split?", "opener_split"),
    ("Image licence check", "opener_image"),
    ("Naming and redirects", "opener_naming"),
)

OPENERS = {
    "opener_lead": (
        "The first paragraph assumes the reader already knows what this is. A general "
        "encyclopedia lead should be readable by someone who came here from a search "
        "result. Proposal: keep the definition in sentence one and push the "
        "qualifications down into “{section}”."
    ),
    "opener_scope": (
        "“{section}” has grown well past what the rest of the article needs. Either it "
        "becomes its own article and we leave a two-sentence summary here, or we cut it "
        "back. I lean towards cutting, because the detail is not what a reader arrives "
        "looking for."
    ),
    "opener_infobox": (
        "Which reference does the infobox figure come from? The body cites a different "
        "value and only one of the two can be right. If nobody can source it I will "
        "remove the row rather than leave an unsourced number in the most visible part "
        "of the page."
    ),
    "opener_split": (
        "This article is carrying two subjects at once: the thing itself and the history "
        "of how it came to be understood. Splitting them would let “{section}” breathe. "
        "Against: readers would then have to visit two pages to get the whole story."
    ),
    "opener_image": (
        "Can someone confirm the licence on the lead image? The credit line is present "
        "but I would like the file page checked before this goes anywhere near the front "
        "page. If the licence is unclear we should replace it, not hope."
    ),
    "opener_naming": (
        "We should decide the canonical title and point every variant at it as a "
        "redirect. Half the incoming links use one spelling and half the other, and the "
        "“what links here” list is unreadable as a result."
    ),
}

REPLIES = (
    "Agreed on the substance. I would keep one sentence of context, though — removing it "
    "entirely makes the next paragraph read as a non sequitur.",
    "Done, and I moved the citation with it so the claim keeps its source.",
    "I checked the source and it supports the weaker version of the claim, not the one in "
    "the article. Rewording rather than removing.",
    "Not convinced. The detail in “{section}” is exactly what distinguishes this article "
    "from the summary a reader could get anywhere else.",
    "Splitting has a cost that is easy to underestimate: two articles means two leads to "
    "keep in step, and they drift.",
    "The file page gives a clear licence and a named author, so the credit line is correct "
    "as written. I have added the source URL as well.",
    "Adding a source. It is not the original paper but it is a review that states the "
    "figure and is freely readable, which is better for a general reader.",
    "I have created the redirects. “What links here” is much easier to read now.",
    "Marking this resolved unless anyone objects in the next week or so.",
    "One more thing while we are here: the section order does not match the chronology in "
    "the body. Worth fixing separately.",
)


# --------------------------------------------------------------------------- #
# The command
# --------------------------------------------------------------------------- #
class Command(BaseCommand):
    help = "Seed the encyclopedia from the CC BY 4.0 corpus in _seed_data/."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--check",
            action="store_true",
            help="Validate the corpus and exit without touching the database.",
        )
        parser.add_argument(
            "--rules",
            action="store_true",
            help="Print the corpus contract this command enforces, and exit.",
        )
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete all existing wiki content first. Requires --force.",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Confirm --flush, or overwrite pre-cutover content.",
        )
        parser.add_argument(
            "--only",
            action="append",
            default=[],
            metavar="SLUG",
            help="Seed only this article slug. Repeatable.",
        )

    # ---- entry point ----------------------------------------------------- #
    def handle(self, *args, **options) -> None:
        if options["rules"]:
            self._print_rules()
            return

        articles = list(ARTICLES)
        if not articles:
            raise CommandError(
                "The corpus is empty. _seed_data/ should hold one module per domain, "
                "each exporting ARTICLES."
            )

        problems = validate_corpus(articles)
        if problems:
            self.stderr.write(
                self.style.ERROR(f"The corpus has {len(problems)} problem(s); nothing was written.")
            )
            for problem in problems:
                self.stderr.write(f"  {problem}")
            raise CommandError(
                "Fix the corpus and run again. `manage.py seed --rules` lists rules."
            )

        notes = storage_notes(articles)
        for note in notes:
            self.stdout.write(self.style.WARNING(f"note: {note}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Corpus valid: {len(articles)} articles from "
                f"{len(_module_names())} modules, {len(RULES)} rules checked."
            )
        )
        if options["check"]:
            return

        selected = self._select(articles, options["only"])

        with transaction.atomic():
            if options["flush"]:
                if not options["force"]:
                    raise CommandError(
                        "--flush deletes every article, revision, talk thread and redirect. "
                        "Re-run as `manage.py seed --flush --force` if that is what you want."
                    )
                self._flush()
            else:
                self._guard_pre_cutover(selected, force=options["force"])

            counts = self._seed(selected, whole_corpus=len(selected) == len(articles))

        self._print_summary(counts)

    # ---- guards ---------------------------------------------------------- #
    def _select(self, articles: list[dict], only: list[str]) -> list[dict]:
        if not only:
            return articles
        wanted = {slug.strip().lower() for slug in only if slug.strip()}
        by_slug = {wiki_slug(article["title"]): article for article in articles}
        unknown = sorted(wanted - set(by_slug))
        if unknown:
            raise CommandError(
                f"No corpus article has the slug(s) {unknown}. "
                f"Known slugs include: {', '.join(sorted(by_slug)[:6])}…"
            )
        return [by_slug[slug] for slug in sorted(wanted)]

    def _guard_pre_cutover(self, articles: list[dict], *, force: bool) -> None:
        """Refuse to rewrite an article this seed did not create (DECISIONS §8).

        Detection is "has at least one revision tagged ``seed``". Evaluated in
        Python rather than with a ``tags__contains`` lookup, which SQLite's JSON1
        backend does not support — and this command must behave identically on
        both databases.
        """
        slugs = {wiki_slug(article["title"]) for article in articles}
        existing = set(Article.objects.filter(slug__in=slugs).values_list("slug", flat=True))
        if not existing:
            return
        seeded: set[str] = set()
        for slug, tags in Revision.objects.filter(article__slug__in=existing).values_list(
            "article__slug", "tags"
        ):
            if isinstance(tags, list) and SEED_TAG in tags:
                seeded.add(slug)
        foreign = sorted(existing - seeded)
        if not foreign:
            return
        if force:
            self.stdout.write(
                self.style.WARNING(
                    f"--force: overwriting {len(foreign)} article(s) this seed did not create: "
                    + ", ".join(foreign[:8])
                    + ("…" if len(foreign) > 8 else "")
                )
            )
            return
        raise CommandError(
            f"{len(foreign)} article(s) already exist with a corpus slug but no seeded "
            f"history, so they are pre-cutover content: {', '.join(foreign[:8])}"
            + ("…" if len(foreign) > 8 else "")
            + ".\n"
            "Seeding over them would rewrite someone else's article. Choose one:\n"
            "  manage.py prune_legacy_seed --force   # remove just the 12 legacy demo "
            "articles, keep everything else\n"
            "  manage.py seed --flush --force        # wipe ALL wiki content and reseed "
            "from the corpus\n"
            "  manage.py seed --force                # keep the rows, overwrite them in place"
        )

    def _flush(self) -> None:
        """Delete every piece of wiki content. Accounts are left alone.

        Deleting users would destroy authorship the migrations deliberately kept
        (``accounts.0003_revoke_legacy_admin``), so the flush stops at content.
        """
        removed = {
            "main page blocks": MainPageBlock.objects.all().delete()[0],
            "watches": Watch.objects.all().delete()[0],
            "talk messages": TalkMessage.objects.all().delete()[0],
            "talk threads": TalkThread.objects.all().delete()[0],
            "links": ArticleLink.objects.all().delete()[0],
            "redirects": Redirect.objects.all().delete()[0],
            "references": Reference.objects.all().delete()[0],
            "revisions": Revision.objects.all().delete()[0],
            "articles": Article.objects.all().delete()[0],
            "categories": Category.objects.all().delete()[0],
        }
        for user in User.objects.all():
            user.recount_edits()
        self.stdout.write(
            self.style.WARNING(
                "Flushed: " + ", ".join(f"{count} {name}" for name, count in removed.items())
            )
        )

    # ---- the seed -------------------------------------------------------- #
    def _seed(self, articles: list[dict], *, whole_corpus: bool) -> dict[str, int]:
        categories = self._seed_categories()
        cast = self._seed_users()

        built: list[tuple[dict, Article]] = []
        counts = dict.fromkeys(
            (
                "categories",
                "articles",
                "revisions",
                "references",
                "redirects",
                "links",
                "red_links",
                "talk_threads",
                "talk_messages",
                "watches",
                "main_page_blocks",
                "users",
            ),
            0,
        )
        counts["categories"] = len(categories)
        counts["users"] = len(cast)

        for data in articles:
            article = self._seed_article(data, categories, cast)
            built.append((data, article))
            counts["articles"] += 1
            counts["references"] += self._seed_references(data, article)
            counts["revisions"] += self._seed_revisions(data, article, cast)

        # Links come last: a red link is only red once every article that *does*
        # exist has been written, so resolving them mid-loop would paint articles
        # red purely because of corpus ordering.
        for _data, article in built:
            ArticleLink.rebuild_for(article)
            ArticleLink.attach_target(article)
        counts["links"] = ArticleLink.objects.count()
        counts["red_links"] = ArticleLink.objects.filter(to_article__isnull=True).count()

        counts["redirects"] = self._seed_redirects(built, cast)

        for data, article in built:
            threads, messages = self._seed_talk(data, article, cast)
            counts["talk_threads"] += threads
            counts["talk_messages"] += messages
            counts["watches"] += self._seed_watches(data, article, cast)

        if whole_corpus:
            counts["main_page_blocks"] = self._seed_main_page(built)
        else:
            counts["main_page_blocks"] = MainPageBlock.objects.count()
            self.stdout.write(
                self.style.WARNING(
                    "--only: main-page blocks left untouched; run a full seed to rebuild them."
                )
            )

        for _data, article in built:
            article.recount()
        for person in cast.values():
            person.recount_edits()
        return counts

    def _seed_categories(self) -> dict[str, Category]:
        categories: dict[str, Category] = {}
        for order, (name, description, color, icon) in enumerate(CATEGORIES):
            category, _created = Category.objects.update_or_create(
                name=name,
                defaults={
                    "description": description,
                    "color": color,
                    "icon": icon,
                    "order": order,
                },
            )
            categories[name] = category
        return categories

    def _seed_users(self) -> dict[str, Any]:
        """Create or refresh the contributor cast.

        Passwords are left unusable on purpose. A seed that installs a known
        password on a public demo is the bug ``accounts.0003`` exists to clean up
        (DECISIONS §8); use ``manage.py ensure_admin`` or the register endpoint.
        """
        cast: dict[str, Any] = {}
        for person in CAST:
            user, created = User.objects.get_or_create(
                username=person.username,
                defaults={"email": f"{person.username}@{CONTRIBUTOR_DOMAIN}"},
            )
            user.first_name = person.first_name
            user.last_name = person.last_name
            user.bio = person.bio
            user.is_bot = person.is_bot
            user.is_staff = False
            user.is_superuser = False
            if created or not user.has_usable_password():
                user.set_unusable_password()
            user.save()
            cast[person.username] = user
        return cast

    def _seed_article(
        self, data: dict, categories: dict[str, Category], cast: dict[str, Any]
    ) -> Article:
        title = data["title"]
        slug = wiki_slug(title)
        rng = rng_for(title, "article")
        author = cast[HUMANS[title_seed(title) % len(HUMANS)].username]
        image = data["image"] or {}

        article, _created = Article.objects.update_or_create(
            slug=slug,
            defaults={
                "title": title,
                "short_description": data["short_description"],
                "summary": data["summary"],
                "content": data["content"],
                "category": categories.get(data["category"]),
                "author": author,
                "last_editor": author,
                "page_type": (
                    Article.PageType.DISAMBIGUATION
                    if data["is_disambiguation"]
                    else Article.PageType.ARTICLE
                ),
                "is_stub": data["is_stub"],
                "protection": self._protection(data),
                "infobox": data["infobox"] or {},
                "lead_image_url": image.get("url", ""),
                "lead_image_alt": image.get("alt", ""),
                "lead_image_caption": image.get("caption", ""),
                "lead_image_credit": image.get("credit", ""),
                "lead_image_license": image.get("license", ""),
                "lead_image_source_url": image.get("source_url", ""),
                "is_published": True,
                "is_deleted": False,
                "deleted_at": None,
                "deleted_by": None,
                "view_count": self._view_count(data, rng),
            },
        )
        extras = [categories[name] for name in data["categories"] if name in categories]
        article.extra_categories.set(extras)
        return article

    @staticmethod
    def _protection(data: dict) -> str:
        """Feature articles are semi-protected one time in three.

        Some variation is needed or the protection badge, the 400 in DECISIONS
        §15 and the "established users only" path have nothing to act on.
        """
        if data["tier"] != "feature":
            return Article.Protection.OPEN
        return (
            Article.Protection.SEMI
            if title_seed(data["title"]) % 3 == 0
            else Article.Protection.OPEN
        )

    @staticmethod
    def _view_count(data: dict, rng: random.Random) -> int:
        ceilings = {"feature": (4000, 26000), "standard": (400, 7000), "stub": (40, 700)}
        low, high = ceilings.get(data["tier"], (100, 2000))
        return rng.randint(low, high)

    def _seed_references(self, data: dict, article: Article) -> int:
        """Write the citations, clamped to their columns.

        ``published_on`` and friends are free text in the contract and fixed-width
        in the model; PostgreSQL rejects the overflow where SQLite silently
        accepts it, so clamp here and let :func:`storage_notes` tell the author.
        """
        keys: list[str] = []
        for order, reference in enumerate(data["references"]):
            Reference.objects.update_or_create(
                article=article,
                key=reference["key"],
                defaults={
                    "order": order,
                    "title": _fit(Reference, "title", reference["title"]),
                    "url": _fit(Reference, "url", reference["url"]),
                    "authors": _fit(Reference, "authors", reference["authors"]),
                    "publisher": _fit(Reference, "publisher", reference["publisher"]),
                    "published_on": _fit(Reference, "published_on", reference["published_on"]),
                    "accessed_on": _iso_date(reference["accessed_on"]),
                    "identifier": _fit(Reference, "identifier", reference["identifier"]),
                    "quote": _fit(Reference, "quote", reference["quote"]),
                },
            )
            keys.append(reference["key"])
        article.references.exclude(key__in=keys).delete()
        return len(keys)

    # ---- synthesised history --------------------------------------------- #
    def _seed_revisions(self, data: dict, article: Article, cast: dict[str, Any]) -> int:
        title = data["title"]
        rng = rng_for(title, "history")
        stages = _revision_stages(data["content"], rng)
        timestamps = _revision_timestamps(len(stages), rng)
        editors = _revision_editors(title, [kind for kind, _body in stages], cast, rng)

        previous = ""
        rows: list[Revision] = []
        for index, ((kind, content), timestamp, editor) in enumerate(
            zip(stages, timestamps, editors, strict=True)
        ):
            size = len(content.encode("utf-8"))
            revision, _created = Revision.objects.update_or_create(
                article=article,
                created_at=timestamp,
                defaults={
                    "editor": editor,
                    "title": title,
                    "summary": data["summary"],
                    "content": content,
                    "comment": _comment(kind, content, previous, rng, editor),
                    "byte_delta": size - len(previous.encode("utf-8")),
                    "is_minor": kind == POLISH,
                    "is_page_creation": kind == CREATE,
                    "is_bot": bool(editor.is_bot),
                    "tags": [SEED_TAG],
                    "apparatus": _apparatus(data, content, last=index == len(stages) - 1),
                },
            )
            rows.append(revision)
            previous = content

        # Parents in a second pass: the chain can only be linked once every row
        # in it has a primary key.
        parent_id: int | None = None
        for revision in rows:
            if revision.parent_id != parent_id:
                revision.parent_id = parent_id
                revision.save(update_fields=["parent"])
            parent_id = revision.pk

        # Drop seeded rows this run did not write — a leftover from an earlier
        # revision count or a different EPOCH. Revisions *without* the seed tag
        # are somebody's real edit and are left alone. The seed-tag test is done
        # in Python because SQLite has no JSON `contains` lookup.
        kept = set(timestamps)
        stale = [
            revision.pk
            for revision in article.revisions.only("id", "created_at", "tags")
            if revision.created_at not in kept
            and isinstance(revision.tags, list)
            and SEED_TAG in revision.tags
        ]
        if stale:
            Revision.objects.filter(pk__in=stale).delete()

        last = rows[-1]
        Article.objects.filter(pk=article.pk).update(
            last_editor=last.editor,
            created_at=rows[0].created_at,
            updated_at=last.created_at,
        )
        article.last_editor = last.editor
        article.created_at = rows[0].created_at
        article.updated_at = last.created_at
        return len(rows)

    # ---- redirects, talk, watches, main page ------------------------------ #
    def _seed_redirects(self, built: list[tuple[dict, Article]], cast: dict[str, Any]) -> int:
        """Redirect rows from ``aliases`` and from the planned redirect table.

        The plan lists all 52 aliases, including those whose target has not been
        written; the ones with no target are skipped and become live the day the
        article is authored.
        """
        by_title = {data["title"]: article for data, article in built}
        pairs: list[tuple[str, str]] = []
        for data, _article in built:
            pairs.extend((alias, data["title"]) for alias in data["aliases"])
        pairs.extend((source, target) for source, target in REDIRECTS if target in by_title)

        taken = set(Article.objects.values_list("slug", flat=True))
        seen: set[str] = set()
        total = 0
        for source, target_title in pairs:
            target = by_title.get(target_title)
            slug = wiki_slug(source)
            # An article always wins a slug, and a reserved slug is unreachable
            # behind a route, so both would produce a dead row (Redirect.clean).
            if target is None or not slug or slug in taken or slug in seen:
                continue
            if slug in RESERVED_SLUGS or slug == target.slug:
                continue
            seen.add(slug)
            Redirect.objects.update_or_create(
                from_slug=slug,
                defaults={
                    "from_title": source,
                    "target": target,
                    "created_by": cast[HUMANS[title_seed(source) % len(HUMANS)].username],
                    "created_at": EPOCH - dt.timedelta(days=title_seed(source) % 900 + 1),
                },
            )
            total += 1
        return total

    def _seed_talk(self, data: dict, article: Article, cast: dict[str, Any]) -> tuple[int, int]:
        """Give roughly two articles in five a discussion.

        Bodies are built from the article's own section headings, so a thread
        reads as though it is about this article rather than about nothing.
        """
        title = data["title"]
        rng = rng_for(title, "talk")
        if rng.random() > 0.42:
            return (0, 0)

        sections = _section_headings(data["content"]) or ["the body"]
        topics = rng.sample(THREAD_TOPICS, 1 if rng.random() > 0.3 else 2)
        people = rng.sample(HUMANS, min(4, len(HUMANS)))
        titles: list[str] = []
        messages_total = 0

        for topic, opener_key in topics:
            section = rng.choice(sections)
            thread_title = topic.format(section=section)[:200]
            titles.append(thread_title)
            opened_at = EPOCH - dt.timedelta(
                days=rng.randint(40, 900), hours=rng.randint(0, 23), minutes=rng.randint(0, 59)
            )
            thread, _created = TalkThread.objects.update_or_create(
                article=article,
                title=thread_title,
                defaults={
                    "created_by": cast[people[0].username],
                    "created_at": opened_at,
                    "is_resolved": rng.random() < 0.35,
                    "is_locked": False,
                },
            )
            bodies = [OPENERS[opener_key].format(section=section)]
            bodies += [
                reply.format(section=section) for reply in rng.sample(REPLIES, rng.randint(1, 4))
            ]
            messages_total += self._seed_thread_messages(thread, bodies, people, cast, rng)

        # Threads from an earlier run with different topics would otherwise pile
        # up, and the thread count would grow on every reseed.
        article.talk_threads.exclude(title__in=titles).delete()
        return (len(titles), messages_total)

    @staticmethod
    def _seed_thread_messages(
        thread: TalkThread,
        bodies: list[str],
        people: list[Contributor],
        cast: dict[str, Any],
        rng: random.Random,
    ) -> int:
        """Write one thread's messages as a shallow reply chain.

        Replies alternate between answering the opener and answering the previous
        message, which is what a real talk page looks like and what exercises the
        nesting the serializer renders.
        """
        kept: list[dt.datetime] = []
        written: list[TalkMessage] = []
        when = thread.created_at
        for index, body in enumerate(bodies):
            if index == 0:
                parent, depth = None, 0
            else:
                parent = written[0] if index % 2 else written[index - 1]
                depth = min(parent.depth + 1, TalkMessage.MAX_DEPTH)
            message, _made = TalkMessage.objects.update_or_create(
                thread=thread,
                created_at=when,
                defaults={
                    "author": cast[people[index % len(people)].username],
                    "body": body,
                    "parent": parent,
                    "depth": depth,
                    "is_deleted": False,
                    "edited_at": None,
                },
            )
            written.append(message)
            kept.append(when)
            when = when + dt.timedelta(
                days=rng.randint(0, 9), hours=rng.randint(1, 20), minutes=rng.randint(0, 59)
            )
        thread.messages.exclude(created_at__in=kept).delete()
        thread.touch()
        return len(kept)

    def _seed_watches(self, data: dict, article: Article, cast: dict[str, Any]) -> int:
        rng = rng_for(data["title"], "watch")
        watchers = rng.sample(HUMANS, rng.randint(0, 3))
        for person in watchers:
            Watch.objects.update_or_create(
                user=cast[person.username],
                article=article,
                defaults={
                    "created_at": EPOCH
                    - dt.timedelta(days=title_seed(person.username + data["title"]) % 700 + 1)
                },
            )
        return len(watchers)

    def _seed_main_page(self, built: list[tuple[dict, Article]]) -> int:
        """Rebuild the three front-page panels.

        The plan's featured rotation names titles that are not written yet, so the
        panel is topped up from the feature tier in corpus order. Nothing here
        assumes six featured articles exist.
        """
        by_title = {data["title"]: article for data, article in built}

        chosen: list[Article] = []
        for title in FEATURED:
            article = by_title.get(title)
            if article is not None and article not in chosen:
                chosen.append(article)
        for data, article in built:
            if len(chosen) >= len(FEATURED):
                break
            if data["tier"] == "feature" and article not in chosen:
                chosen.append(article)

        # ``(kind, position)`` is the natural key, so reseeding updates the rows in
        # place instead of renumbering them. The front page is cached by
        # ``stats_epoch()``, and churning ids would invalidate that for nothing.
        wanted: list[tuple[str, int, dict[str, Any]]] = [
            (MainPageBlock.Kind.FEATURED, position, {"article": article, "body_markdown": ""})
            for position, article in enumerate(chosen)
        ]
        wanted += [
            (MainPageBlock.Kind.DYK, position, {"article": None, "body_markdown": hook})
            for position, hook in enumerate(DID_YOU_KNOW)
        ]
        wanted += [
            (
                MainPageBlock.Kind.OTD,
                position,
                {
                    "article": None,
                    "body_markdown": body,
                    "event_year": year,
                    "event_month": month,
                    "event_day": day,
                },
            )
            for position, (year, month, day, body) in enumerate(ON_THIS_DAY)
        ]

        keys: list[tuple[str, int]] = []
        for kind, position, defaults in wanted:
            MainPageBlock.objects.update_or_create(
                kind=kind,
                position=position,
                defaults={
                    "event_year": None,
                    "event_month": None,
                    "event_day": None,
                    "is_active": True,
                    **defaults,
                },
            )
            keys.append((kind, position))
        for block in MainPageBlock.objects.all().only("id", "kind", "position"):
            if (block.kind, block.position) not in keys:
                block.delete()
        return len(keys)

    # ---- output ---------------------------------------------------------- #
    def _print_rules(self) -> None:
        self.stdout.write(self.style.MIGRATE_HEADING("Seed corpus contract (DECISIONS §19)"))
        width = max(len(name) for name, _text in RULES)
        for name, text in RULES:
            self.stdout.write(f"  {name.ljust(width)}  {text}")
        self.stdout.write(
            "\nA [[wikilink]] to a planned but unwritten title is a valid red link, not an "
            "error.\nThe link universe is the 120 planned titles, not the articles that exist."
        )

    def _print_summary(self, counts: dict[str, int]) -> None:
        self.stdout.write(self.style.MIGRATE_HEADING("Seed complete"))
        labels = (
            ("categories", "categories"),
            ("articles", "articles"),
            ("revisions", "revisions"),
            ("references", "references"),
            ("redirects", "redirects"),
            ("links", "links (total)"),
            ("red_links", "links (red)"),
            ("talk_threads", "talk threads"),
            ("talk_messages", "talk messages"),
            ("watches", "watches"),
            ("main_page_blocks", "main page blocks"),
            ("users", "contributors"),
        )
        width = max(len(label) for _key, label in labels)
        for key, label in labels:
            self.stdout.write(f"  {label.ljust(width)}  {counts[key]:>6}")
        self.stdout.write(
            self.style.SUCCESS(
                "No superuser was created. Run `manage.py ensure_admin` for admin access."
            )
        )


# --------------------------------------------------------------------------- #
# History synthesis helpers
# --------------------------------------------------------------------------- #
def _blocks(content: str) -> list[str]:
    """Split a body into paragraph-ish blocks, keeping fenced code together."""
    parts: list[str] = []
    buffer: list[str] = []
    in_fence = False
    for line in (content or "").split("\n"):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            buffer.append(line)
            continue
        if not stripped and not in_fence:
            if buffer:
                parts.append("\n".join(buffer).strip())
                buffer = []
            continue
        buffer.append(line)
    if buffer:
        parts.append("\n".join(buffer).strip())
    return [part for part in parts if part]


def _revision_stages(content: str, rng: random.Random) -> list[tuple[str, str]]:
    """``[(kind, body)]`` — how the article looked at each revision, oldest first.

    The article *grows*: the creation carries the lead and the opening sections
    and each later ``grow`` appends more blocks, so a diff between any two
    revisions shows real added prose rather than noise. The last stage is always
    the published text exactly, which is what makes the newest revision a
    faithful snapshot and ``POST /restore/`` meaningful.

    Some middle revisions are ``polish`` instead: the body is unchanged, the
    revision is flagged minor, and its summary is drawn from the pool of edits
    that genuinely move no bytes (punctuation, hyphenation, a typo, a bot sweep).
    That is what gives Recent changes its ``m`` and ``b`` flags and its zero
    ``byte_delta`` rows something honest to show. Prose is never mutated to
    manufacture a delta — the corpus text is the corpus authors' work.
    """
    blocks = _blocks(content)
    total = len(blocks)
    count = rng.randint(MIN_REVISIONS, MAX_REVISIONS)
    if total <= 1:
        # Nothing to grow through: a creation and one polish pass.
        return [(CREATE, content), (POLISH, content)]

    # Polish slots are strictly interior, so the creation is always first and a
    # grow holding the published text is always last.
    interior = max(0, count - 2)
    polish_wanted = rng.randint(0, (interior + 1) // 2) if interior else 0
    growth_total = count - polish_wanted
    if growth_total > total:
        # More growth steps than there are blocks to add would make some of them
        # add nothing, and a "grow" that changes no bytes is exactly the row a
        # reviewer spots as generated. Spend the surplus on polish instead.
        polish_wanted += growth_total - total
        growth_total = total

    polish_at: set[int] = set()
    if polish_wanted:
        polish_at = set(rng.sample(range(1, count - 1), polish_wanted))

    stages: list[tuple[str, str]] = []
    body = ""
    rank = 0
    for index in range(count):
        if index in polish_at:
            stages.append((POLISH, body))
            continue
        rank += 1
        keep = total if rank == growth_total else max(1, round(total * rank / growth_total))
        body = content if keep >= total else "\n\n".join(blocks[:keep])
        stages.append((CREATE if index == 0 else GROW, body))
    return stages


def _revision_timestamps(count: int, rng: random.Random) -> list[dt.datetime]:
    """``count`` strictly increasing instants ending shortly before :data:`EPOCH`.

    The day offsets are sampled *without replacement*, so no two revisions of one
    article can land on the same instant — which matters because ``created_at`` is
    the natural key this command uses to make reseeding idempotent.
    """
    oldest = rng.randint(420, 2400)
    newest = rng.randint(3, 120)
    if count == 1:
        offsets = [newest]
    else:
        middle = rng.sample(range(newest + 1, oldest), count - 2) if count > 2 else []
        offsets = sorted([oldest, newest, *middle], reverse=True)
    return [
        EPOCH
        - dt.timedelta(
            days=days,
            hours=rng.randint(0, 23),
            minutes=rng.randint(0, 59),
            seconds=rng.randint(0, 59),
        )
        for days in offsets
    ]


def _revision_editors(
    title: str, kinds: list[str], cast: dict[str, Any], rng: random.Random
) -> list[Any]:
    """Rotate authorship across the cast, with the bot only on polish edits.

    The bot's summaries are whitespace and punctuation sweeps, so putting it on a
    revision that adds two sections would make the history read as generated. It
    only ever gets a ``polish`` slot, which is a genuine no-op to the text.
    """
    creator = HUMANS[title_seed(title) % len(HUMANS)]
    editors = [cast[creator.username]]
    for index, kind in enumerate(kinds[1:], start=1):
        if kind == POLISH and rng.random() < 0.55:
            editors.append(cast["wikiverse-bot"])
            continue
        person = HUMANS[(title_seed(title) + index * 3) % len(HUMANS)]
        if rng.random() < 0.25:
            person = rng.choice(HUMANS)
        editors.append(cast[person.username])
    return editors


def _comment(kind: str, content: str, previous: str, rng: random.Random, editor: Any) -> str:
    """A plausible edit summary for this revision's kind.

    A ``grow`` revision names the section it actually added, taken from the body
    — which is why the history reads as though somebody wrote it.
    """
    if kind == CREATE:
        return rng.choice(CREATION_SUMMARIES)
    if kind == POLISH:
        pool = BOT_SUMMARIES if getattr(editor, "is_bot", False) else POLISH_SUMMARIES
        return rng.choice(pool)
    added = _section_headings(content[len(previous) :])
    if not added:
        return rng.choice(GROWTH_SUMMARIES)
    if len(added) == 1:
        return f'Added the "{added[0]}" section'[:255]
    return f'Added "{added[0]}" and {len(added) - 1} more section(s)'[:255]


def _section_headings(markdown: str) -> list[str]:
    """``##``-level headings, in order, text only."""
    headings: list[str] = []
    for line in (markdown or "").split("\n"):
        stripped = line.strip()
        if stripped.startswith("##") and not stripped.startswith("####"):
            headings.append(stripped.lstrip("#").strip())
    return headings


def _apparatus(data: dict, content: str, *, last: bool) -> dict[str, Any]:
    """The non-column snapshot, matching what ``ArticleViewSet._snapshot`` writes.

    Older revisions carry only the references their own text cites, and no
    infobox: it was "added" partway through the history. The newest revision
    carries everything, so ``POST /restore/`` is lossless.
    """
    cited = set(count_footnotes(content))
    references = [
        {
            "key": reference["key"],
            "order": order,
            "title": reference["title"],
            "url": reference["url"],
            "authors": reference["authors"],
            "publisher": reference["publisher"],
            "published_on": reference["published_on"],
            "accessed_on": reference["accessed_on"] or None,
            "identifier": reference["identifier"],
            "quote": reference["quote"],
        }
        for order, reference in enumerate(data["references"])
        if last or reference["key"] in cited
    ]
    return {
        "references": references,
        "infobox": (data["infobox"] or {}) if last else {},
        "categories": [data["category"], *data["categories"]],
        "short_description": data["short_description"],
    }


# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #
def _fit(model: type, field_name: str, value: str) -> str:
    """Clamp ``value`` to the column's ``max_length``.

    Reads the limit off the model rather than repeating the number, so a widened
    column takes effect here without an edit.
    """
    limit = model._meta.get_field(field_name).max_length
    text = value or ""
    return text if limit is None else text[:limit]


def _iso_date(value: str) -> dt.date | None:
    if not value:
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:  # pragma: no cover - the validator rejects these first
        return None


def _module_names() -> list[str]:
    from . import _seed_data

    return _seed_data.iter_modules()
