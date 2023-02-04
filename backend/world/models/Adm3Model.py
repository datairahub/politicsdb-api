# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstracModel


class Adm3(BaseAbstracModel):
    """
    Region
    """

    name = models.CharField(max_length=100, db_index=True)
    code = models.CharField(
        max_length=30, db_index=True, unique=True
    )  # es_sev_aljarafe
    adm0 = models.ForeignKey(
        "world.Adm0", null=False, on_delete=models.PROTECT, related_name="adm3"
    )
    adm1 = models.ForeignKey(
        "world.Adm1", null=False, on_delete=models.PROTECT, related_name="adm3"
    )
    adm2 = models.ForeignKey(
        "world.Adm2", null=False, on_delete=models.PROTECT, related_name="adm3"
    )

    def __str__(self):
        return f"{self.name} ({self.adm0.iso_name})"

    class Meta:
        ordering = ("id",)
        verbose_name = "Adm3"
        verbose_name_plural = "Adm3"
