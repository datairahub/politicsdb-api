# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstractModel


class Position(BaseAbstractModel):
    """
    Cargo en institución (parlamentario, senador...)
    """

    short_name = models.CharField(
        max_length=255,
        help_text="Nombre corto del cargo (Diputado, Ministro...)",
    )
    full_name = models.TextField(
        help_text="Nombre oficial del cargo (Diputado de la Legislatura VII...)",
    )
    person = models.ForeignKey(
        "people.Person",
        on_delete=models.CASCADE,
        related_name="positions",
        help_text="Persona que ostenta el cargo",
    )
    period = models.ForeignKey(
        "positions.Period",
        on_delete=models.CASCADE,
        related_name="positions",
        help_text="Periodo vinculado al cargo",
    )
    candidacy = models.ForeignKey(
        "organizations.Candidacy",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="positions",
        help_text="Candidatura que consigue el cargo",
    )
    start = models.DateField(
        help_text="Fecha de inicio del cargo",
    )
    end = models.DateField(
        help_text="Fecha de finalización del cargo",
    )

    def __str__(self):
        return f"{self.person.full_name} - {self.full_name}"

    class Meta(BaseAbstractModel.Meta):
        db_table = "positions_position"
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
