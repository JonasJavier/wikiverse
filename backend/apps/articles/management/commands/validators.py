"""The seed corpus validator — the gate in front of ``manage.py seed``.

``validate_corpus(articles)`` returns a list of human-readable problems. Every
line names the article and the rule that was broken, so a content author can act
on the output without reading this file::

    Zero: [short-description-length] short_description is 97 characters; the
    limit is 90.

The rules are DECISIONS §19 and nothing else. Two consequences of that are worth
stating plainly because they invert the obvious expectation:

* **A link to a title that has not been written yet is valid.** The link
  universe is the 120 planned titles in :data:`meta.PLANNED_TITLES`, not the
  articles that happen to exist. A target inside the plan but absent from the
  corpus is a *red link* and passes; only a target outside the plan fails
  (DECISIONS §19, RED LINKS).
* **Nothing here counts the corpus.** 63 articles is as valid as 120.

Parsing is delegated to :mod:`apps.articles.markup` and infobox checking to
:func:`apps.articles.infobox.validate_infobox` — the same code the renderer and
the model field use. A second, independent parser here would drift, and the day
it drifted the validator would bless markup the renderer could not draw.

:func:`storage_notes` is separate and advisory. It reports values that are
legal under §19 but wider than the database column they land in — ``published_on``
is declared free text by the contract and is a ``varchar(40)`` in the model, so
the two can disagree without either being wrong. The seed prints those notes and
clamps; it does not refuse.
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable, Sequence
from typing import Any
from urllib.parse import urlsplit

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from apps.articles.infobox import validate_infobox
from apps.articles.markup import count_footnotes, extract_wikilinks, mask_code
from apps.articles.models import Article, Reference
from apps.common.utils import RESERVED_SLUGS, wiki_slug

from ._seed_data.meta import PLANNED_TITLES, VALID_CATEGORY_NAMES

__all__ = [
    "IMAGE_KEYS",
    "KINDS",
    "MAX_SHORT_DESCRIPTION",
    "MAX_SUMMARY",
    "REFERENCE_KEYS",
    "RULES",
    "SEED_KEYS",
    "TIERS",
    "storage_notes",
    "validate_corpus",
]

#: The exact key set of a ``SeedArticle`` (DECISIONS §19). Not a subset, not a
#: superset: a typo'd key would otherwise be silently dropped by the seed.
SEED_KEYS: frozenset[str] = frozenset(
    {
        "title",
        "category",
        "categories",
        "short_description",
        "summary",
        "content",
        "tier",
        "kind",
        "infobox",
        "image",
        "references",
        "see_also",
        "aliases",
        "is_stub",
        "is_disambiguation",
        "tags",
    }
)

REFERENCE_KEYS: frozenset[str] = frozenset(
    {
        "key",
        "title",
        "url",
        "authors",
        "publisher",
        "published_on",
        "accessed_on",
        "identifier",
        "quote",
    }
)

IMAGE_KEYS: frozenset[str] = frozenset({"url", "alt", "caption", "credit", "license", "source_url"})

TIERS: tuple[str, ...] = ("feature", "standard", "stub")

KINDS: tuple[str, ...] = (
    "concept",
    "person",
    "place",
    "work",
    "period",
    "discipline",
    "disambiguation",
)

MAX_SHORT_DESCRIPTION = 90
MAX_SUMMARY = 300

#: Every rule this module enforces, in the order it is checked. Printed by
#: ``manage.py seed --rules`` so the contract is discoverable from the CLI
#: instead of only from DECISIONS.md.
RULES: tuple[tuple[str, str], ...] = (
    ("article-shape", "Each article is a dict with exactly the 16 SeedArticle keys."),
    ("field-types", "Every field has the declared type; strings are non-empty where required."),
    ("title-planned", "The title is one of the 120 titles in the content plan."),
    ("title-unique", "Titles are unique, and no two titles slugify to the same slug."),
    ("slug-reserved", "The title does not slugify to a reserved slug such as 'search'."),
    ("category-valid", "`category` is one of the 16 taxonomy names."),
    (
        "categories-valid",
        "`categories` holds valid extra names, deduplicated, without the primary.",
    ),
    ("short-description-length", f"`short_description` is at most {MAX_SHORT_DESCRIPTION} chars."),
    ("short-description-period", "`short_description` does not end in a period."),
    ("summary-length", f"`summary` is at most {MAX_SUMMARY} chars."),
    ("tier-valid", "`tier` is feature, standard or stub."),
    ("kind-valid", "`kind` is one of the seven declared kinds."),
    ("stub-consistent", "`is_stub` agrees with tier == 'stub'."),
    ("disambiguation-consistent", "`is_disambiguation` agrees with kind == 'disambiguation'."),
    ("no-h1", "The body has no level-one heading; it starts at `##`."),
    ("no-handwritten-sections", "The body hand-writes neither `## See also` nor `## References`."),
    ("no-raw-html", "The body contains no raw HTML; it would be stripped."),
    ("bold-lead", "The first sentence opens by restating the title in bold."),
    ("wikilink-planned", "Every [[wikilink]] target is a planned title (red links are valid)."),
    ("see-also-planned", "Every see_also entry is a planned title, not self, not repeated."),
    ("reference-shape", "Each reference has exactly the 9 declared keys."),
    ("reference-key", "Reference keys are slugs, unique within the article, usable in [^key]."),
    ("reference-accessed-on", "`accessed_on` is an ISO YYYY-MM-DD date or empty."),
    ("footnote-resolves", "Every [^marker] resolves to a reference key in the same article."),
    ("reference-cited", "Every reference is cited by at least one [^marker]."),
    ("infobox-shape", "`infobox` matches the closed DECISIONS §1 schema, and carries no image."),
    ("image-shape", "`image` has exactly the 6 declared keys, all non-empty strings."),
    ("image-host", "`image.url` is https on a settings.LEAD_IMAGE_ALLOWED_HOSTS host."),
    ("alias-unique", "An alias shadows no real title and collides with no other alias."),
    ("alias-slug", "An alias does not slugify onto an article slug or a reserved slug."),
    ("tags-valid", "`tags` holds short, non-empty, deduplicated strings."),
)

_ATX_H1_RE = re.compile(r"^[ \t]{0,3}#[ \t]", re.M)
_SETEXT_H1_RE = re.compile(r"^(?P<text>\S[^\n]*)\n[ \t]{0,3}=+[ \t]*$", re.M)
_SEE_ALSO_HEADING_RE = re.compile(r"^[ \t]{0,3}#{1,6}[ \t]*see[ \t]+also\b", re.M | re.I)
_REFERENCES_HEADING_RE = re.compile(
    r"^[ \t]{0,3}#{1,6}[ \t]*(references|citations|notes|bibliography|sources)\b", re.M | re.I
)
_HTML_RE = re.compile(r"</?[A-Za-z][A-Za-z0-9-]*(?:\s[^<>\n]{0,200})?/?>|<!--")
#: The lead may open with a short article ("The **Fourier transform** is …").
_BOLD_LEAD_RE = re.compile(r"^\s*(?:the|a|an)?\s*\*\*(?P<bold>[^*\n]{1,160})\*\*", re.I)
_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
#: The intersection of what ``markup._FOOTNOTE_RE`` will match in ``[^key]`` and
#: what Django's ``SlugField`` will store in ``Reference.key``. The marker regex
#: also accepts ``.`` and ``:``; the column does not, so those are out.
_SLUG_KEY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,59}$")
_WORD_RE = re.compile(r"[0-9a-z]+")

MAX_TAG_LENGTH = 40


# --------------------------------------------------------------------------- #
# Entry points
# --------------------------------------------------------------------------- #
def validate_corpus(articles: Sequence[dict[str, Any]]) -> list[str]:
    """Return every contract problem in ``articles``, or an empty list.

    Corpus-wide rules (title uniqueness, alias collisions) need the whole set, so
    this takes the concatenated corpus rather than one article at a time.
    """
    problems: list[str] = []
    rows = list(articles)

    shaped: list[dict[str, Any]] = []
    for index, article in enumerate(rows):
        if not isinstance(article, dict):
            problems.append(
                f"article #{index}: [article-shape] expected a dict, got {type(article).__name__}."
            )
            continue
        title = article.get("title")
        if not isinstance(title, str) or not title.strip():
            problems.append(f"article #{index}: [field-types] `title` must be a non-empty string.")
            continue
        missing = sorted(SEED_KEYS - set(article))
        unknown = sorted(set(article) - SEED_KEYS)
        if missing:
            problems.append(f"{title}: [article-shape] missing keys: {missing}.")
        if unknown:
            problems.append(f"{title}: [article-shape] unknown keys: {unknown}.")
        if missing:
            # Per-article rules index into the keys; without them they would all
            # report the same absence.
            continue
        shaped.append(article)

    for article in shaped:
        problems.extend(_validate_article(article))
    problems.extend(_validate_corpus_wide(shaped))
    return problems


def storage_notes(articles: Sequence[dict[str, Any]]) -> list[str]:
    """Return advisory notes about values wider than their database column.

    Not a §19 violation — ``published_on`` is *declared* free text — but on
    PostgreSQL a ``varchar(40)`` refuses a 45-character string, so the seed
    clamps and says so rather than dying halfway through a transaction.
    """
    notes: list[str] = []
    for article in articles:
        title = str(article.get("title", "?"))
        for key, field_name in (
            ("title", "title"),
            ("short_description", "short_description"),
            ("summary", "summary"),
        ):
            notes.extend(_width_note(title, "article", key, article.get(key), Article, field_name))
        image = article.get("image")
        if isinstance(image, dict):
            for key, field_name in (
                ("url", "lead_image_url"),
                ("alt", "lead_image_alt"),
                ("caption", "lead_image_caption"),
                ("credit", "lead_image_credit"),
                ("license", "lead_image_license"),
                ("source_url", "lead_image_source_url"),
            ):
                notes.extend(_width_note(title, "image", key, image.get(key), Article, field_name))
        for reference in article.get("references") or []:
            if not isinstance(reference, dict):
                continue
            where = f"reference '{reference.get('key', '?')}'"
            for key in ("key", "title", "url", "authors", "publisher", "published_on"):
                notes.extend(_width_note(title, where, key, reference.get(key), Reference, key))
            for key in ("identifier", "quote"):
                notes.extend(_width_note(title, where, key, reference.get(key), Reference, key))
    return notes


def _width_note(
    title: str, where: str, key: str, value: object, model: type, field_name: str
) -> list[str]:
    limit = model._meta.get_field(field_name).max_length
    if not isinstance(value, str) or limit is None or len(value) <= limit:
        return []
    return [
        f"{title}: {where}.{key} is {len(value)} characters and "
        f"{model.__name__}.{field_name} holds {limit}; the seed will clamp it."
    ]


# --------------------------------------------------------------------------- #
# Per-article rules
# --------------------------------------------------------------------------- #
def _validate_article(article: dict[str, Any]) -> list[str]:
    title = str(article["title"])
    problems: list[str] = []
    report = _reporter(problems, title)

    if title.strip() != title:
        report("field-types", "`title` has leading or trailing whitespace.")
    if title not in PLANNED_TITLES:
        report(
            "title-planned",
            "the title is not in the content plan, so nothing can link to it; "
            "add it to docs/content-plan.json first.",
        )
    slug = wiki_slug(title)
    if not slug:
        report("title-unique", "the title slugifies to nothing.")
    elif slug in RESERVED_SLUGS:
        report("slug-reserved", f"the title slugifies to the reserved slug '{slug}'.")

    problems.extend(_validate_classification(article, title))
    problems.extend(_validate_prose_fields(article, title))
    problems.extend(_validate_body(article, title))
    problems.extend(_validate_references(article, title))
    problems.extend(_validate_infobox(article, title))
    problems.extend(_validate_image(article, title))
    problems.extend(_validate_lists(article, title))
    return problems


def _validate_classification(article: dict[str, Any], title: str) -> list[str]:
    problems: list[str] = []
    report = _reporter(problems, title)

    category = article["category"]
    if not isinstance(category, str) or category not in VALID_CATEGORY_NAMES:
        report(
            "category-valid",
            f"`category` is {category!r}; it must be one of the 16 taxonomy names.",
        )

    extras = article["categories"]
    if not isinstance(extras, list):
        report("field-types", f"`categories` must be a list, not {type(extras).__name__}.")
    else:
        for name in extras:
            if not isinstance(name, str) or name not in VALID_CATEGORY_NAMES:
                report("categories-valid", f"extra category {name!r} is not a taxonomy name.")
            elif name == category:
                report(
                    "categories-valid",
                    f"`categories` repeats the primary category {name!r}; "
                    "the primary one stays in `category` only.",
                )
        duplicates = sorted({n for n, count in Counter(extras).items() if count > 1})
        if duplicates:
            report("categories-valid", f"`categories` repeats {duplicates}.")

    tier = article["tier"]
    if tier not in TIERS:
        report("tier-valid", f"`tier` is {tier!r}; expected one of {list(TIERS)}.")
    kind = article["kind"]
    if kind not in KINDS:
        report("kind-valid", f"`kind` is {kind!r}; expected one of {list(KINDS)}.")

    is_stub = article["is_stub"]
    if not isinstance(is_stub, bool):
        report("field-types", "`is_stub` must be a bool.")
    elif is_stub != (tier == "stub"):
        report(
            "stub-consistent",
            f"`is_stub` is {is_stub} but `tier` is {tier!r}; they must agree.",
        )

    is_disambiguation = article["is_disambiguation"]
    if not isinstance(is_disambiguation, bool):
        report("field-types", "`is_disambiguation` must be a bool.")
    elif is_disambiguation != (kind == "disambiguation"):
        report(
            "disambiguation-consistent",
            f"`is_disambiguation` is {is_disambiguation} but `kind` is {kind!r}; they must agree.",
        )
    return problems


def _validate_prose_fields(article: dict[str, Any], title: str) -> list[str]:
    problems: list[str] = []
    report = _reporter(problems, title)

    short = article["short_description"]
    if not isinstance(short, str) or not short.strip():
        report("field-types", "`short_description` must be a non-empty string.")
    else:
        if len(short) > MAX_SHORT_DESCRIPTION:
            report(
                "short-description-length",
                f"`short_description` is {len(short)} characters; the limit is "
                f"{MAX_SHORT_DESCRIPTION}.",
            )
        if short.rstrip().endswith("."):
            report(
                "short-description-period",
                "`short_description` ends in a period; it is a tagline, not a sentence.",
            )

    summary = article["summary"]
    if not isinstance(summary, str) or not summary.strip():
        report("field-types", "`summary` must be a non-empty string.")
    elif len(summary) > MAX_SUMMARY:
        report("summary-length", f"`summary` is {len(summary)} characters; the limit is 300.")

    content = article["content"]
    if not isinstance(content, str) or not content.strip():
        report("field-types", "`content` must be a non-empty string.")
    return problems


def _validate_body(article: dict[str, Any], title: str) -> list[str]:
    problems: list[str] = []
    report = _reporter(problems, title)
    content = article["content"]
    if not isinstance(content, str) or not content.strip():
        return problems

    # Headings and HTML are structural, so look at the body with code masked —
    # a '# comment' inside a fenced block is not a heading.
    masked = mask_code(content)

    if _ATX_H1_RE.search(masked):
        report(
            "no-h1", "the body has a `# ` heading; the page renders the title, so start at `##`."
        )
    setext = _SETEXT_H1_RE.search(masked)
    if setext:
        report(
            "no-h1",
            f"the body underlines {setext.group('text').strip()[:40]!r} with '=', "
            "which is a level-one heading.",
        )
    if _SEE_ALSO_HEADING_RE.search(masked):
        report(
            "no-handwritten-sections",
            "the body hand-writes a 'See also' heading; it is rendered from `see_also`.",
        )
    if _REFERENCES_HEADING_RE.search(masked):
        report(
            "no-handwritten-sections",
            "the body hand-writes a references heading; it is rendered from `references`.",
        )
    html = _HTML_RE.search(masked)
    if html:
        report(
            "no-raw-html", f"the body contains raw HTML ({html.group(0)[:30]!r}); it is stripped."
        )

    lead = _BOLD_LEAD_RE.match(content)
    if lead is None:
        report(
            "bold-lead",
            "the body does not open by restating the title in bold "
            "(`**Photosynthesis** is the process…`).",
        )
    elif not _restates(lead.group("bold"), title):
        report(
            "bold-lead",
            f"the opening bold text {lead.group('bold').strip()[:50]!r} does not restate "
            f"the title {title!r}.",
        )

    for target, _display in _all_wikilinks(article):
        if target not in PLANNED_TITLES:
            report(
                "wikilink-planned",
                f"[[{target}]] is in neither the corpus nor the content plan. A link to a "
                "planned-but-unwritten title is a valid red link; this one is a typo or a "
                "missing plan entry.",
            )
    return problems


def _validate_references(article: dict[str, Any], title: str) -> list[str]:
    problems: list[str] = []
    report = _reporter(problems, title)

    references = article["references"]
    if not isinstance(references, list):
        report("field-types", f"`references` must be a list, not {type(references).__name__}.")
        return problems

    keys: list[str] = []
    for index, reference in enumerate(references):
        where = f"references[{index}]"
        if not isinstance(reference, dict):
            report("reference-shape", f"{where} must be a dict.")
            continue
        missing = sorted(REFERENCE_KEYS - set(reference))
        unknown = sorted(set(reference) - REFERENCE_KEYS)
        if missing:
            report("reference-shape", f"{where} is missing keys: {missing}.")
        if unknown:
            report("reference-shape", f"{where} has unknown keys: {unknown}.")
        for field, value in reference.items():
            if field in REFERENCE_KEYS and not isinstance(value, str):
                report(
                    "reference-shape",
                    f"{where}.{field} must be a string, not {type(value).__name__}.",
                )
        key = reference.get("key")
        if isinstance(key, str):
            keys.append(key)
            if not _SLUG_KEY_RE.match(key):
                report(
                    "reference-key",
                    f"reference key {key!r} must be letters, digits, hyphens or underscores "
                    "(at most 60, starting with a letter or digit) so `[^key]` can address it "
                    "and Reference.key can store it.",
                )
        if not str(reference.get("title") or "").strip():
            report("reference-shape", f"{where}.title must not be empty.")
        url = str(reference.get("url") or "")
        if url and not url.startswith(("http://", "https://")):
            report("reference-shape", f"{where}.url is not an absolute URL: {url[:40]!r}.")
        accessed = str(reference.get("accessed_on") or "")
        if accessed and not _ISO_DATE_RE.match(accessed):
            report(
                "reference-accessed-on",
                f"{where}.accessed_on is {accessed!r}; it must be an ISO YYYY-MM-DD date.",
            )

    duplicates = sorted({k for k, count in Counter(keys).items() if count > 1})
    if duplicates:
        report("reference-key", f"reference keys are repeated: {duplicates}.")

    declared = set(keys)
    cited = set(_all_footnotes(article))
    for key in sorted(cited - declared):
        report(
            "footnote-resolves",
            f"the marker [^{key}] resolves to no reference in this article.",
        )
    for key in sorted(declared - cited):
        report("reference-cited", f"reference {key!r} is never cited by a [^{key}] marker.")
    return problems


def _validate_infobox(article: dict[str, Any], title: str) -> list[str]:
    problems: list[str] = []
    report = _reporter(problems, title)
    infobox = article["infobox"]
    if infobox is None:
        return problems
    try:
        # The model field's own validator, so the corpus cannot carry an infobox
        # the API would reject on write.
        validate_infobox(infobox)
    except ValidationError as exc:
        for message in exc.messages:
            report("infobox-shape", message)
    return problems


def _validate_image(article: dict[str, Any], title: str) -> list[str]:
    problems: list[str] = []
    report = _reporter(problems, title)
    image = article["image"]
    if image is None:
        return problems
    if not isinstance(image, dict):
        report("image-shape", f"`image` must be a dict or None, not {type(image).__name__}.")
        return problems

    missing = sorted(IMAGE_KEYS - set(image))
    unknown = sorted(set(image) - IMAGE_KEYS)
    if missing:
        report("image-shape", f"`image` is missing keys: {missing}.")
    if unknown:
        report("image-shape", f"`image` has unknown keys: {unknown}.")
    for key in sorted(IMAGE_KEYS & set(image)):
        value = image[key]
        if not isinstance(value, str) or not value.strip():
            report(
                "image-shape",
                f"`image.{key}` must be a non-empty string; an image without alt text, a "
                "credit and a licence cannot be published.",
            )

    url = image.get("url")
    if isinstance(url, str) and url:
        allowed = [host.lower() for host in getattr(settings, "LEAD_IMAGE_ALLOWED_HOSTS", [])]
        parts = urlsplit(url)
        if parts.scheme != "https" or not parts.netloc:
            report("image-host", f"`image.url` must be an absolute https URL, got {url[:50]!r}.")
        elif parts.netloc.lower() not in allowed:
            report(
                "image-host",
                f"`image.url` is hosted on {parts.netloc!r}; the CSP img-src allowlist is "
                + ", ".join(allowed)
                + ".",
            )
    source_url = image.get("source_url")
    if isinstance(source_url, str) and source_url and not source_url.startswith("https://"):
        report("image-shape", "`image.source_url` must be an absolute https URL.")
    return problems


def _validate_lists(article: dict[str, Any], title: str) -> list[str]:
    problems: list[str] = []
    report = _reporter(problems, title)

    see_also = article["see_also"]
    if not isinstance(see_also, list):
        report("field-types", f"`see_also` must be a list, not {type(see_also).__name__}.")
    else:
        for entry in see_also:
            if not isinstance(entry, str):
                report("see-also-planned", f"see_also entry {entry!r} is not a string.")
            elif entry == title:
                report("see-also-planned", "see_also points at this article itself.")
            elif entry not in PLANNED_TITLES:
                report(
                    "see-also-planned",
                    f"see_also entry {entry!r} is not a planned title. Unwritten planned "
                    "titles are fine — they render as red links — but this one is unknown.",
                )
        duplicates = sorted({e for e, count in Counter(see_also).items() if count > 1})
        if duplicates:
            report("see-also-planned", f"see_also repeats {duplicates}.")

    tags = article["tags"]
    if not isinstance(tags, list):
        report("field-types", f"`tags` must be a list, not {type(tags).__name__}.")
    else:
        for tag in tags:
            if not isinstance(tag, str) or not tag.strip():
                report("tags-valid", f"tag {tag!r} must be a non-empty string.")
            elif len(tag) > MAX_TAG_LENGTH:
                report("tags-valid", f"tag {tag!r} is longer than {MAX_TAG_LENGTH} characters.")
        duplicates = sorted({t for t, count in Counter(tags).items() if count > 1})
        if duplicates:
            report("tags-valid", f"tags repeat {duplicates}.")

    aliases = article["aliases"]
    if not isinstance(aliases, list):
        report("field-types", f"`aliases` must be a list, not {type(aliases).__name__}.")
    else:
        for alias in aliases:
            if not isinstance(alias, str) or not alias.strip():
                report("alias-unique", f"alias {alias!r} must be a non-empty string.")
                continue
            if alias == title:
                report("alias-unique", f"alias {alias!r} is the article's own title.")
            alias_slug = wiki_slug(alias)
            if not alias_slug:
                report("alias-slug", f"alias {alias!r} slugifies to nothing.")
            elif alias_slug in RESERVED_SLUGS:
                report("alias-slug", f"alias {alias!r} slugifies to reserved slug {alias_slug!r}.")
            elif alias_slug == wiki_slug(title):
                report(
                    "alias-slug",
                    f"alias {alias!r} slugifies onto this article's own slug {alias_slug!r}.",
                )
        duplicates = sorted({a for a, count in Counter(aliases).items() if count > 1})
        if duplicates:
            report("alias-unique", f"aliases repeat {duplicates}.")
    return problems


# --------------------------------------------------------------------------- #
# Corpus-wide rules
# --------------------------------------------------------------------------- #
def _validate_corpus_wide(articles: Sequence[dict[str, Any]]) -> list[str]:
    problems: list[str] = []
    titles = [str(article["title"]) for article in articles]

    for title, count in sorted(Counter(titles).items()):
        if count > 1:
            problems.append(f"{title}: [title-unique] the title appears {count} times.")

    by_slug: dict[str, list[str]] = {}
    for title in titles:
        by_slug.setdefault(wiki_slug(title), []).append(title)
    for slug, sharing in sorted(by_slug.items()):
        if len(set(sharing)) > 1:
            problems.append(
                f"{sorted(set(sharing))[0]}: [title-unique] {sorted(set(sharing))} all "
                f"slugify to '{slug}', so only one of them would be reachable."
            )

    title_set = set(titles)
    slug_set = set(by_slug)
    alias_owner: dict[str, str] = {}
    alias_slug_owner: dict[str, str] = {}
    for article in articles:
        title = str(article["title"])
        aliases = article["aliases"]
        if not isinstance(aliases, list):
            continue
        for alias in aliases:
            if not isinstance(alias, str) or not alias.strip():
                continue
            if alias in title_set:
                problems.append(
                    f"{title}: [alias-unique] alias {alias!r} is also a real article title; "
                    "the article would always win and the redirect would be dead."
                )
            owner = alias_owner.setdefault(alias, title)
            if owner != title:
                problems.append(
                    f"{title}: [alias-unique] alias {alias!r} is already claimed by {owner!r}."
                )
            alias_slug = wiki_slug(alias)
            if alias_slug and alias_slug in slug_set:
                problems.append(
                    f"{title}: [alias-slug] alias {alias!r} slugifies to '{alias_slug}', which "
                    "an article already uses."
                )
            slug_owner = alias_slug_owner.setdefault(alias_slug, title)
            if alias_slug and slug_owner != title:
                problems.append(
                    f"{title}: [alias-slug] alias {alias!r} slugifies to '{alias_slug}', which "
                    f"an alias of {slug_owner!r} already uses."
                )
    return problems


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _reporter(problems: list[str], title: str):
    def report(rule: str, message: str) -> None:
        problems.append(f"{title}: [{rule}] {message}")

    return report


def _infobox_values(article: dict[str, Any]) -> Iterable[str]:
    """Row values of the article's infobox, which carry markup of their own."""
    infobox = article.get("infobox")
    if not isinstance(infobox, dict):
        return
    for row in infobox.get("rows") or []:
        if isinstance(row, dict):
            yield str(row.get("value") or "")


def _all_wikilinks(article: dict[str, Any]) -> list[tuple[str, str]]:
    """Wikilinks in the body **and** in infobox row values.

    ``ArticleLink.link_targets`` scans both, so the validator must too, or a
    typo'd link inside the side panel would pass here and become a red link the
    author never asked for.
    """
    content = article.get("content")
    links = extract_wikilinks(content) if isinstance(content, str) else []
    for value in _infobox_values(article):
        links.extend(extract_wikilinks(value))
    return links


def _all_footnotes(article: dict[str, Any]) -> dict[str, int]:
    content = article.get("content")
    counts = dict(count_footnotes(content)) if isinstance(content, str) else {}
    for value in _infobox_values(article):
        for key, count in count_footnotes(value).items():
            counts[key] = counts.get(key, 0) + count
    return counts


def _restates(bold: str, title: str) -> bool:
    """True when the opening bold text is a fair restatement of ``title``.

    Titles are disambiguated ("Mercury (planet)") and leads are natural
    ("**Mercury** is the smallest planet", "**Steam engines** were…"), so this
    compares runs of words rather than characters, and folds a trailing plural
    ``s`` so a plural lead still matches a singular title.
    """
    bold_words = _fold(bold)
    title_words = _fold(re.sub(r"\(.*?\)", " ", title))
    if not bold_words or not title_words:
        return False
    return _contains(title_words, bold_words) or _contains(bold_words, title_words)


def _fold(text: str) -> list[str]:
    """Significant words, lowercased, with a trailing plural ``s`` removed."""
    return [
        word[:-1] if len(word) > 3 and word.endswith("s") else word
        for word in _WORD_RE.findall(text.lower())
    ]


def _contains(haystack: list[str], needle: list[str]) -> bool:
    return any(
        haystack[start : start + len(needle)] == needle
        for start in range(len(haystack) - len(needle) + 1)
    )


# --------------------------------------------------------------------------- #
# ``manage.py validators``
# --------------------------------------------------------------------------- #
# Django's command discovery lists every non-underscore module in a `commands/`
# package, so this file appears in `manage.py help` whether or not it wants to.
# A listed command that raises AttributeError when invoked is a worse outcome
# than a useful one, so it is a real command: validate the corpus and print the
# contract. It is exactly what `manage.py seed --check` does, without loading the
# seed.
class Command(BaseCommand):
    help = "Validate the seed corpus against the DECISIONS §19 contract."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--rules",
            action="store_true",
            help="Print the rule list instead of validating.",
        )

    def handle(self, *args, **options) -> None:
        from ._seed_data import ARTICLES, iter_modules

        if options["rules"]:
            width = max(len(name) for name, _text in RULES)
            for name, text in RULES:
                self.stdout.write(f"  {name.ljust(width)}  {text}")
            return

        problems = validate_corpus(ARTICLES)
        for note in storage_notes(ARTICLES):
            self.stdout.write(self.style.WARNING(f"note: {note}"))
        if problems:
            for problem in problems:
                self.stderr.write(f"  {problem}")
            raise CommandError(f"The corpus has {len(problems)} problem(s).")
        self.stdout.write(
            self.style.SUCCESS(
                f"Corpus valid: {len(ARTICLES)} articles from {len(iter_modules())} modules, "
                f"{len(RULES)} rules checked."
            )
        )
