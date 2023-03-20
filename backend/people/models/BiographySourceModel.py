# -*- coding: utf-8 -*-
from django.db import models
from core.models import DataSourceAbstractModel


class BiographySource(DataSourceAbstractModel):
    """
    Fuente de biografía
    """

    value = models.TextField(null=False, blank=False, help_text="Biografía")

    class Meta(DataSourceAbstractModel.Meta):
        db_table = "people_biographysource"
        verbose_name = "Biografía"
        verbose_name_plural = "Biografías"
