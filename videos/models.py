from autoslug import AutoSlugField as SlugField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    SearchVectorField,
)
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from contrib.models import TimestampMixin

from .validators import NameValidator, VideoValidator


class VideoQuerySet(models.QuerySet):
    def search(self, term):
        if not term:
            return self.none()
        sq = SearchQuery(term, config="portuguese")
        return (
            self.annotate(rank=SearchRank("search", sq))
            .filter(search=sq)
            .order_by("-rank")
        )


class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    def search(self, term):
        return self.get_queryset().search(term)


class Video(TimestampMixin, models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    slug = SlugField(populate_from="title", unique=True)
    media = models.FileField(
        upload_to="videos/", validators=[NameValidator(), VideoValidator()]
    )
    search = SearchVectorField(null=True)
    objects = VideoManager()

    class Meta:
        db_table = "videos"
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")
        ordering = ["-created_at"]
        indexes = [
            GinIndex(fields=["search"]),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.refresh_from_db()
        self.search = SearchVector("title")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("video-detail", kwargs={"slug": self.slug})
