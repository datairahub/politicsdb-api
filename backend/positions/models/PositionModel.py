# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstracModel


class Position(BaseAbstracModel):
    """
    Cargo en institución (parlamentario, senador...)
    """

    person = models.ForeignKey("persons.Person", on_delete=models.CASCADE)
    institution = models.ForeignKey("positions.Institution", on_delete=models.PROTECT)
    period = models.ForeignKey("positions.Period", on_delete=models.PROTECT)
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
