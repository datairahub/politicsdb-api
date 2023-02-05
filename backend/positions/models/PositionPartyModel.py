# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstracModel


class PositionParty(BaseAbstracModel):
    """
    Representación del cargo por partido
    """

    position = models.ForeignKey(
        "positions.Position",
        on_delete=models.CASCADE,
        related_name="positionparties",
    )
    party = models.ForeignKey(
        "organizations.Party",
        on_delete=models.PROTECT,
        related_name="positionparties",
    )
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            (
                "position",
                "party",
            ),
        )
