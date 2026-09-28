"""Regressions in the article write path found by the browser suite."""

import pytest

from apps.articles.models import Article


@pytest.mark.django_db
def test_null_infobox_is_saved_as_empty(auth_client, article):
    """The editor sends ``infobox: null`` for an article without one.

    Rejecting it made every save of an infobox-less article fail with a 400.
    """
    response = auth_client.patch(
        f"/api/articles/{article.slug}/",
        {"content": "Django is a web framework.\n\nEdited.", "infobox": None, "comment": "x"},
        format="json",
    )

    assert response.status_code == 200, response.content
    article.refresh_from_db()
    assert article.infobox == {}
    assert article.content.endswith("Edited.")


@pytest.mark.django_db
def test_invalid_infobox_is_still_rejected(auth_client, article):
    response = auth_client.patch(
        f"/api/articles/{article.slug}/",
        {"infobox": {"rows": [{"kind": "row", "label": "A", "value": {"nested": 1}}]}},
        format="json",
    )

    assert response.status_code == 400
    assert "infobox" in response.json()
    assert Article.objects.get(pk=article.pk).infobox == {}
