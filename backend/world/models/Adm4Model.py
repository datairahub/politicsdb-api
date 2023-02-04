# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstracModel


class Adm4(BaseAbstracModel):
    """
    City
    """

    name = models.CharField(max_length=100, db_index=True)
    code = models.CharField(
        max_length=30, db_index=True, unique=True
    )  # es_sev_castillejadelacuesta
    adm0 = models.ForeignKey(
        "world.Adm0", null=False, on_delete=models.PROTECT, related_name="adm4"
    )
    adm1 = models.ForeignKey(
        "world.Adm1", null=False, on_delete=models.PROTECT, related_name="adm4"
    )
    adm2 = models.ForeignKey(
        "world.Adm2", null=False, on_delete=models.PROTECT, related_name="adm4"
    )
    adm3 = models.ForeignKey(
        "world.Adm3", null=False, on_delete=models.PROTECT, related_name="adm4"
    )

    def __str__(self):
        return f"{self.name} ({self.adm0.name})"

    class Meta:
        ordering = ("id",)
        verbose_name = "Adm4"
        verbose_name_plural = "Adm4"
