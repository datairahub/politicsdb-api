# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstractModel


class Party(BaseAbstractModel):
    """
    Partido político (nivel nacional)
    """

    name = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Nombre completo del partido político",
    )
    short_name = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Siglas del partido político",
    )
    color = models.CharField(
        max_length=7,
        help_text="Color principal del partido político",
    )
    adm0 = models.ForeignKey(
        "world.Adm0",
        null=True,
        on_delete=models.PROTECT,
        related_name="parties",
        help_text="País al que pertenece el partido político",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("id",)
        db_table = "organizations_party"
        verbose_name = "Partido"
        verbose_name_plural = "Partidos"
        unique_together = (
            ("name", "adm0"),
            ("short_name", "adm0"),
        )
