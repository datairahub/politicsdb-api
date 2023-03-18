# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstractModel


class Adm1(BaseAbstractModel):
    """
    Autonomous Community
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
        help_text="Código completo (<adm0>_<adm1>): es_and para España-Andalucía",
    )
    adm0 = models.ForeignKey(
        "world.Adm0",
        null=False,
        on_delete=models.PROTECT,
        related_name="adm1",
        help_text="Adm0 al que pertenece",
    )

    def __str__(self):
        return f"{self.name} ({self.adm0.iso_name})"

    class Meta(BaseAbstractModel.Meta):
        verbose_name = "Adm1"
        verbose_name_plural = "Adm1"
