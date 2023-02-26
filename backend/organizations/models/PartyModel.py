# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstracModel


class Party(BaseAbstracModel):
    """
    Partido político (global)
    """

    name = models.CharField(
        max_length=255,
        db_index=True,
    )
    short_name = models.CharField(
        max_length=255,
        db_index=True,
    )
    color = models.CharField(
        max_length=7,
    )
    adm0 = models.ForeignKey(
        "world.Adm0",
        null=True,
        on_delete=models.PROTECT,
        related_name="parties",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("id",)
        verbose_name_plural = "Parties"
        unique_together = (
            ("name", "adm0"),
            ("short_name", "adm0"),
        )
