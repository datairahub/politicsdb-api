# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstractModel


class Period(BaseAbstractModel):
    """
    Periodo en una institución (legislatura X del Congreso...)
    """

    name = models.CharField(
        max_length=250,
        db_index=True,
        help_text="Nombre formal del periodo (Legislatura X)",
    )
    number = models.IntegerField(
        help_text="Número del periodo (orden)",
    )
    code = models.CharField(
        max_length=250,
        db_index=True,
        help_text="Código del período (V, VI, VII...)",
    )
    institution = models.ForeignKey(
        "positions.Institution",
        on_delete=models.PROTECT,
        related_name="periods",
        help_text="Institución a la que pertenece el periodo",
    )
    start = models.DateField(
        help_text="Fecha de inicio del periodo",
    )
    end = models.DateField(
        help_text="Fecha de finalización del periodo",
    )

    def __str__(self):
        return f"{self.institution.name} - {self.name}"

    class Meta(BaseAbstractModel.Meta):
        db_table = "positions_period"
        verbose_name = "Periodo"
        verbose_name_plural = "Periodos"
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
