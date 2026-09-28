"""``manage.py seed_e2e`` — the minimum fixture a browser test can rely on.

DECISIONS §18 fixes this contract exactly: **one** category and **exactly** the
slugs ``e2e-read-me``, ``e2e-edit-me`` and ``e2e-talk-me``, each with **two**
revisions, and **no superuser**. A browser test asserts on those slugs, so they
are not adjustable.

Deliberately not the real seed: 63 articles make an end-to-end run slow, and a
test that asserts "the first search result is X" against real content breaks the
day somebody improves an article. This fixture is small enough to reason about
and boring enough to stay stable.

Idempotent, and independent of ``manage.py seed``: the two never share rows,
because these slugs are not in the corpus.
"""

from __future__ import annotations

import datetime as dt

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.articles.models import (
    Article,
    ArticleLink,
    Category,
    Revision,
    TalkMessage,
    TalkThread,
)

User = get_user_model()

#: Fixed instants, so a test may assert on rendered dates.
EPOCH = dt.datetime(2026, 9, 1, 12, 0, tzinfo=dt.UTC)

CATEGORY_NAME = "E2E Fixtures"

E2E_USERNAME = "e2e-author"
E2E_EMAIL = "e2e-author@fixtures.wikiverse.invalid"

#: ``(slug, title, short_description, summary, body)``. The bodies stay short:
#: a test scrolls them.
PAGES: tuple[tuple[str, str, str, str, str], ...] = (
    (
        "e2e-read-me",
        "E2E read me",
        "A fixture article that end-to-end tests only read",
        "A stable fixture article for end-to-end tests that assert on reading an article.",
        "**E2E read me** is a fixture article. End-to-end tests read it and assert on the "
        "rendered result, so its text does not change.\n\n"
        "## Structure\n\n"
        "It has one heading so that the table of contents has something to build, and a link "
        "to [[E2E edit me]] so that “what links here” has a row.\n\n"
        "## Stability\n\n"
        "Nothing in this article is interesting. That is the point.",
    ),
    (
        "e2e-edit-me",
        "E2E edit me",
        "A fixture article that end-to-end tests edit",
        "A stable fixture article for end-to-end tests that assert on editing and history.",
        "**E2E edit me** is a fixture article that end-to-end tests modify.\n\n"
        "## Editing\n\n"
        "A test signs in, changes this paragraph, and asserts that a new revision appears in "
        "the history with its edit summary. It links back to [[E2E read me]].",
    ),
    (
        "e2e-talk-me",
        "E2E talk me",
        "A fixture article whose talk page end-to-end tests post to",
        "A stable fixture article for end-to-end tests that assert on talk threads and replies.",
        "**E2E talk me** is a fixture article used by talk-page tests.\n\n"
        "## Discussion\n\n"
        "Its talk page starts with one thread holding one message, so a test can assert on "
        "both an existing thread and a newly posted reply.",
    ),
)

#: The second revision's edit summary, so a history assertion has a known string.
SECOND_REVISION_COMMENT = "Second revision, created by seed_e2e"


class Command(BaseCommand):
    help = "Create the minimal end-to-end test fixture (1 category, 3 articles, 2 revisions each)."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete the fixture rows first. Only touches the e2e-* slugs.",
        )

    @transaction.atomic
    def handle(self, *args, **options) -> None:
        slugs = [slug for slug, *_rest in PAGES]
        if options["flush"]:
            Article.objects.filter(slug__in=slugs).delete()
            Category.objects.filter(name=CATEGORY_NAME).delete()
            self.stdout.write(self.style.WARNING("Flushed the e2e fixture."))

        category, _created = Category.objects.update_or_create(
            name=CATEGORY_NAME,
            defaults={
                "description": "Fixtures for end-to-end tests. Not encyclopedia content.",
                "color": "#4f7d93",
                "icon": "flask-conical",
                "order": 99,
            },
        )
        author, created = User.objects.get_or_create(
            username=E2E_USERNAME,
            defaults={"email": E2E_EMAIL},
        )
        author.bio = "Fixture account used by the end-to-end suite."
        author.is_staff = False
        author.is_superuser = False
        if created or not author.has_usable_password():
            # No superuser and no known password: a test that needs to sign in
            # registers its own account through the API.
            author.set_unusable_password()
        author.save()

        articles: list[Article] = []
        for slug, title, short_description, summary, body in PAGES:
            article = self._page(slug, title, short_description, summary, body, category, author)
            articles.append(article)

        for article in articles:
            ArticleLink.rebuild_for(article)
            ArticleLink.attach_target(article)

        self._talk(articles[-1], author)

        for article in articles:
            article.recount()
        author.recount_edits()

        self.stdout.write(
            self.style.SUCCESS(
                f"e2e fixture ready: 1 category, {len(articles)} articles, "
                f"{Revision.objects.filter(article__in=articles).count()} revisions, "
                f"{TalkThread.objects.filter(article__in=articles).count()} talk thread(s). "
                "No superuser was created."
            )
        )

    def _page(
        self,
        slug: str,
        title: str,
        short_description: str,
        summary: str,
        body: str,
        category: Category,
        author,
    ) -> Article:
        article, _created = Article.objects.update_or_create(
            slug=slug,
            defaults={
                "title": title,
                "short_description": short_description,
                "summary": summary,
                "content": body,
                "category": category,
                "author": author,
                "last_editor": author,
                "page_type": Article.PageType.ARTICLE,
                "is_stub": False,
                "protection": Article.Protection.OPEN,
                "infobox": {},
                "is_published": True,
                "is_deleted": False,
                "view_count": 7,
            },
        )
        # Exactly two revisions: the creation, holding the lead only, and the
        # current text. A test can therefore diff revision 1 against revision 2
        # and see a real change.
        lead = body.split("\n\n", 1)[0]
        stages = (
            (EPOCH - dt.timedelta(days=2), lead, "Created the article", True),
            (EPOCH - dt.timedelta(days=1), body, SECOND_REVISION_COMMENT, False),
        )
        previous = 0
        parent = None
        kept: list[dt.datetime] = []
        for when, content, comment, is_creation in stages:
            size = len(content.encode("utf-8"))
            revision, _made = Revision.objects.update_or_create(
                article=article,
                created_at=when,
                defaults={
                    "parent": parent,
                    "editor": author,
                    "title": title,
                    "summary": summary,
                    "content": content,
                    "comment": comment,
                    "byte_delta": size - previous,
                    "is_minor": False,
                    "is_page_creation": is_creation,
                    "is_bot": False,
                    "tags": ["seed", "e2e"],
                    "apparatus": {
                        "references": [],
                        "infobox": {},
                        "categories": [category.name],
                        "short_description": short_description,
                    },
                },
            )
            parent = revision
            previous = size
            kept.append(when)
        article.revisions.exclude(created_at__in=kept).delete()
        Article.objects.filter(pk=article.pk).update(created_at=kept[0], updated_at=kept[-1])
        return article

    def _talk(self, article: Article, author) -> None:
        thread, _created = TalkThread.objects.update_or_create(
            article=article,
            title="Fixture thread",
            defaults={
                "created_by": author,
                "created_at": EPOCH - dt.timedelta(hours=12),
                "is_resolved": False,
                "is_locked": False,
            },
        )
        when = EPOCH - dt.timedelta(hours=12)
        TalkMessage.objects.update_or_create(
            thread=thread,
            created_at=when,
            defaults={
                "author": author,
                "body": "This thread exists so that a test can assert on an existing message "
                "and then post a reply to it.",
                "parent": None,
                "depth": 0,
                "is_deleted": False,
            },
        )
        thread.messages.exclude(created_at=when).delete()
        thread.touch()
