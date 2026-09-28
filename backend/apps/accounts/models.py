from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user with a public profile.

    Kept username-based for simplicity, but ``email`` is required and unique so
    it can be used for account recovery and notifications.
    """

    email = models.EmailField("email address", unique=True)
    bio = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    edit_count = models.PositiveIntegerField(
        default=0,
        editable=False,
        help_text="Denormalised revision count. Drives semi-protection and the history byline.",
    )
    is_bot = models.BooleanField(
        default=False,
        help_text="Marks automated edits with the 'b' flag in Recent changes.",
    )

    class Meta:
        ordering = ["username"]
        indexes = [models.Index(fields=["-edit_count"], name="user_edit_count_desc")]

    def __str__(self) -> str:
        return self.username

    @property
    def article_count(self) -> int:
        """Articles this user created that are publicly visible.

        Filtered, because an unfiltered count leaks the existence of drafts.
        """
        return self.articles.filter(is_published=True, is_deleted=False).count()

    def recount_edits(self, *, save: bool = True) -> int:
        """Re-derive :attr:`edit_count` from the revision table."""
        self.edit_count = self.revisions.count()
        if save and self.pk is not None:
            self.save(update_fields=["edit_count"])
        return self.edit_count
