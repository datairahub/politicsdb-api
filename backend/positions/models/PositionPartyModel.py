# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstracModel


class PositionParty(BaseAbstracModel):
    """
    Representación del cargo por partido
    """

    position = models.ForeignKey("positions.Position", on_delete=models.CASCADE)
    period = models.ForeignKey("positions.Period", on_delete=models.PROTECT)
    party = models.ForeignKey("organizations.Party", on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            (
                "position",
                "period",
                "party",
            ),
        )
