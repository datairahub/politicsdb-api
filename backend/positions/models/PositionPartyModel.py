# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstractModel


class PositionParty(BaseAbstractModel):
    """
    Representación del cargo en nombre de partido
    """

    position = models.ForeignKey(
        "positions.Position",
        on_delete=models.CASCADE,
        related_name="positionparties",
        help_text="Cargo al que hace referencia",
    )
    party = models.ForeignKey(
        "organizations.Party",
        on_delete=models.PROTECT,
        related_name="positionparties",
        help_text="Partido por el que se ostenta el cargo",
    )
    start = models.DateField(
        help_text="Fecha de inicio del cargo por el partido",
    )
    end = models.DateField(
        help_text="Fecha de finalización del cargo por el partido",
    )

    def __str__(self):
        return self.name

    class Meta(BaseAbstractModel.Meta):
        db_table = "positions_position_party"
        verbose_name = "Cargo por Partido"
        verbose_name_plural = "Cargos por Partido"
        unique_together = (
            (
                "position",
                "party",
            ),
        )
