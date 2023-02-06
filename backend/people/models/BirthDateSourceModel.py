# -*- coding: utf-8 -*-
from urllib.parse import urlparse
from django.db import models
from core.models import BaseAbstracModel


class BirthDateSource(BaseAbstracModel):
    """
    Fuente (informativa) para la fecha de nacimiento
    """

    person = models.ForeignKey(
        "people.Person",
        on_delete=models.CASCADE,
        related_name="BirthDateSources",
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
    is_exact = models.BooleanField(
        default=False,
    )
    date = models.DateField()

    def pre_save(self, *args, **kwargs):
        self.name = urlparse(self.url).netloc
        super().pre_save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("person", "url"),)
