# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstractModel


class PositionFoundation(BaseAbstractModel):
    """
    Cargo en fundación (secreatario, fundador...)
    """

    name = models.TextField(
        help_text="Nombre oficial del cargo (Secretario, Presidenta...)",
    )
    person = models.ForeignKey(
        "people.Person",
        on_delete=models.CASCADE,
        related_name="foundation_positions",
        help_text="Persona que ostenta el cargo",
    )
    foundation = models.ForeignKey(
        "organizations.Foundation",
        on_delete=models.CASCADE,
        related_name="foundation_positions",
        help_text="Fundación a la que pertenece el cargo",
    )
    start = models.DateField(
        help_text="Fecha de inicio del cargo",
    )
    end = models.DateField(
        help_text="Fecha de finalización del cargo",
    )

    def __str__(self):
        return f"{self.person.full_name} - {self.name} de {self.foundation.full_name}"

    class Meta(BaseAbstractModel.Meta):
        db_table = "positions_foundationposition"
        verbose_name = "Cargo en fundación"
        verbose_name_plural = "Cargos en fundaciones"
