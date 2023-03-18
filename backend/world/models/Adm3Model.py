# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstractModel


class Adm3(BaseAbstractModel):
    """
    Region
    """

    name = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Nombre completo",
    )
    code = models.CharField(
        max_length=100,
        db_index=True,
        unique=True,
        help_text="Código completo (<adm0>_<adm3>): es_sev_aljarafe para España-Aljarafe",
    )
    adm0 = models.ForeignKey(
        "world.Adm0",
        null=False,
        on_delete=models.PROTECT,
        related_name="adm3",
        help_text="Adm0 al que pertenece",
    )
    adm1 = models.ForeignKey(
        "world.Adm1",
        null=False,
        on_delete=models.PROTECT,
        related_name="adm3",
        help_text="Adm1 al que pertenece",
    )
    adm2 = models.ForeignKey(
        "world.Adm2",
        null=False,
        on_delete=models.PROTECT,
        related_name="adm3",
        help_text="Adm2 al que pertenece",
    )

    def __str__(self):
        return f"{self.name} ({self.adm0.iso_name})"

    class Meta(BaseAbstractModel.Meta):
        verbose_name = "Adm3"
        verbose_name_plural = "Adm3"
