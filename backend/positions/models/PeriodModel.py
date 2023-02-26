# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstracModel


class Period(BaseAbstracModel):
    """
    Periodo en una institución (legislatura X del Congreso...)
    """

    name = models.CharField(
        max_length=250,
        db_index=True,
    )
    number = models.IntegerField()
    code = models.CharField(
        max_length=250,
        db_index=True,
    )
    institution = models.ForeignKey(
        "positions.Institution",
        on_delete=models.PROTECT,
        related_name="periods",
    )
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return f"{self.institution.name} - {self.name}"

    class Meta:
        ordering = ("id",)
        unique_together = (
            (
                "name",
                "institution",
            ),
            (
                "number",
                "institution",
            ),
            (
                "code",
                "institution",
            ),
        )
