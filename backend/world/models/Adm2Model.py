# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstracModel


class Adm2(BaseAbstracModel):
    """
    Province
    """

    name = models.CharField(max_length=100, db_index=True)
    code = models.CharField(max_length=6, db_index=True, unique=True)  # es_sev
    adm0 = models.ForeignKey(
        "world.Adm0", null=False, on_delete=models.PROTECT, related_name="adm2"
    )
    adm1 = models.ForeignKey(
        "world.Adm1", null=False, on_delete=models.PROTECT, related_name="adm2"
    )

    def __str__(self):
        return f"{self.name} ({self.adm0.iso_name})"

    class Meta:
        ordering = ("id",)
        verbose_name = "Adm2"
        verbose_name_plural = "Adm2"
