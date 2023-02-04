# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstracModel


class Position(BaseAbstracModel):
    """
    Cargo en institución (parlamentario, senador...)
    """

    short_name = models.CharField(max_length=255)
    full_name = models.TextField()
    person = models.ForeignKey("people.Person", on_delete=models.CASCADE)
    period = models.ForeignKey("positions.Period", on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return f"{self.person.full_name} - {self.full_name}"
