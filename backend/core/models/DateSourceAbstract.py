# -*- coding: utf-8 -*-
from django.contrib.gis.db import models

from core.models import DataSourceAbstractModel
from core.validators import validate_partial_date


class DateSourceAbstractModel(DataSourceAbstractModel):
    ACCURACY = (
        (1, "Year"),
        (2, "Year-Month"),
        (3, "Year-Month-Day"),
    )
    value = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        help_text="Fecha en crudo. Formato YYYY o YYYY-MM o YYYY-MM-DD",
        validators=[validate_partial_date],
    )
    date = models.DateField(
        help_text="Fecha formateada",
    )
    accuracy = models.IntegerField(
        null=False,
        blank=False,
        choices=ACCURACY,
        help_text="Precisión de la fecha",
    )

    def save(self, *args, **kwargs):
        if len(self.value) == 10:
            self.date = self.value
            self.accuracy = 3
        elif len(self.value) == 7:
            self.date = f"{self.value}-01"
            self.accuracy = 2
        elif len(self.value) == 4:
            self.date = f"{self.value}-01-01"
            self.accuracy = 1
        super().save(*args, **kwargs)

    class Meta(DataSourceAbstractModel.Meta):
        abstract = True
