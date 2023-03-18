# -*- coding: utf-8 -*-
from urllib.parse import urlparse
from django.contrib.gis.db import models

from core.models import BaseModel


class DataSourceAbstractModel(BaseModel):
    person = models.ForeignKey(
        "people.Person",
        on_delete=models.CASCADE,
        help_text="Persona a la que pertenece la biografía",
    )
    name = models.CharField(
        max_length=255,
        db_index=True,
        null=False,
        blank=False,
        help_text="Dominio de la fuente",
    )
    url = models.TextField(
        null=False, blank=False, help_text="Url completa de la fuente"
    )

    def save(self, *args, **kwargs):
        self.name = urlparse(self.url).netloc
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        abstract = True
        unique_together = (("person", "url"),)
