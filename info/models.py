from django.db import models
from django.utils.translation import gettext_lazy as _


class Movies(models.Model):
    """
    Represents a movie with its name, genre, and rating.
    Stores the latest 10 movies fetched from TMDB.
    """
    name = models.CharField(max_length=255, verbose_name=_("Movie Name"))
    genre = models.CharField(max_length=255, verbose_name=_("Genre"))
    rating = models.DecimalField(max_digits=3, decimal_places=1, verbose_name=_("Rating"))
    tmdb_id = models.IntegerField(unique=True, verbose_name=_("TMDB ID"))
    poster_path = models.URLField(blank=True, null=True, verbose_name=_("Poster URL"))
    overview = models.TextField(blank=True, null=True, verbose_name=_("Overview"))
    release_date = models.DateField(blank=True, null=True, verbose_name=_("Release Date"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")
        ordering = ('-release_date',)

    def __str__(self):
        """
        String representation of the Movies model instance.
        """
        return self.name
