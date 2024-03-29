# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstractModel


class PositionParty(BaseAbstractModel):
    """
    Cargo en partido político (secretario, fundador...)
    """

    name = models.TextField(
        help_text="Nombre oficial del cargo (Secretario, Presidenta...)",
    )
    person = models.ForeignKey(
        "people.Person",
        on_delete=models.CASCADE,
        related_name="party_positions",
        help_text="Persona que ostenta el cargo",
    )
    party = models.ForeignKey(
        "organizations.Party",
        on_delete=models.CASCADE,
        related_name="party_positions",
        help_text="Partido al que pertenece el cargo",
    )
    start = models.DateField(
        help_text="Fecha de inicio del cargo",
    )
    end = models.DateField(
        help_text="Fecha de finalización del cargo",
    )

    def __str__(self):
        return f"{self.person.full_name} - {self.name} de {self.party.full_name}"

    class Meta(BaseAbstractModel.Meta):
        db_table = "positions_partyposition"
        verbose_name = "Cargo en partido"
        verbose_name_plural = "Cargos en partidos"
