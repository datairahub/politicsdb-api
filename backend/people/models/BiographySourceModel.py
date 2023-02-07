# -*- coding: utf-8 -*-
from urllib.parse import urlparse
from django.db import models
from core.models import BaseAbstracModel


class BiographySource(BaseAbstracModel):
    """
    Fuente (informativa) para la biografía (descripción)
    """

    person = models.ForeignKey(
        "people.Person",
        on_delete=models.CASCADE,
        related_name="biographysources",
    )
    name = models.CharField(
        max_length=255,
        db_index=True,
        null=False,
        blank=False,
    )
    url = models.TextField(
        null=False,
        blank=False,
    )
    bio = models.TextField(
        null=False,
        blank=False,
    )

    def pre_save(self, *args, **kwargs):
        self.name = urlparse(self.url).netloc
        super().pre_save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("person", "url"),)
