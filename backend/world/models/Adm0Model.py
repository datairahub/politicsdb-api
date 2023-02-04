# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstracModel


class Adm0(BaseAbstracModel):
    """
    Country
    """

    name = models.CharField(max_length=100, db_index=True)
    iso_name = models.CharField(max_length=100, db_index=True)
    code = models.CharField(max_length=2, db_index=True, unique=True)

    def __str__(self):
        return f"{self.name} ({self.iso_name})"

    class Meta:
        ordering = ("id",)
        verbose_name = "Adm0"
        verbose_name_plural = "Adm0"
