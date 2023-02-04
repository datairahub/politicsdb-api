# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstracModel


class Period(BaseAbstracModel):
    """
    Periodo en institución (legislatura...)
    """

    name = models.CharField(max_length=250, db_index=True)
    number = models.IntegerField()
    code = models.CharField(max_length=250, db_index=True)
    institution = models.ForeignKey("positions.Institution", on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
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
