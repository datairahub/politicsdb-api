# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstracModel


class Adm1(BaseAbstracModel):
    """
    Autonomous Community
    """

    name = models.CharField(max_length=100, db_index=True)
    code = models.CharField(max_length=6, db_index=True, unique=True)  # es_and
    adm0 = models.ForeignKey(
        "world.Adm0", null=False, on_delete=models.PROTECT, related_name="adm1"
    )

    def __str__(self):
        return f"{self.name} ({self.adm0.iso_name})"

    class Meta:
        ordering = ("id",)
        verbose_name = "Adm1"
        verbose_name_plural = "Adm1"
