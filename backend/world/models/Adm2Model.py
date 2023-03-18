# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstractModel


class Adm2(BaseAbstractModel):
    """
    Province
    """

    name = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Nombre completo",
    )
    code = models.CharField(
        max_length=6,
        db_index=True,
        unique=True,
        help_text="Código completo (<adm0>_<adm2>): es_sev para España-Sevilla",
    )
    adm0 = models.ForeignKey(
        "world.Adm0",
        null=False,
        on_delete=models.PROTECT,
        related_name="adm2",
        help_text="Adm0 al que pertenece",
    )
    adm1 = models.ForeignKey(
        "world.Adm1",
        null=False,
        on_delete=models.PROTECT,
        related_name="adm2",
        help_text="Adm1 al que pertenece",
    )

    def __str__(self):
        return f"{self.name} ({self.adm0.iso_name})"

    class Meta(BaseAbstractModel.Meta):
        verbose_name = "Adm2"
        verbose_name_plural = "Adm2"
