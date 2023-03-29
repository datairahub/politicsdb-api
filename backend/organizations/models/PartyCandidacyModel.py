# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstractModel


class PartyCandidacy(BaseAbstractModel):
    """
    Acuerdo por partido de formar parte de una candidatura
    """

    date = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha del acuerdo",
    )
    candidacy = models.ForeignKey(
        "organizations.Candidacy",
        on_delete=models.CASCADE,
        related_name="party_candidatures",
        help_text="Candidatura a la que hace referencia",
    )
    party = models.ForeignKey(
        "organizations.Party",
        on_delete=models.CASCADE,
        related_name="party_candidatures",
        help_text="Partido al que hace referencia",
    )
    source = models.TextField(
        null=False, blank=False, help_text="Url completa de la fuente"
    )

    class Meta:
        ordering = ("id",)
        db_table = "organizations_partycandidacy"
        verbose_name = "Participación en candidatura"
        verbose_name_plural = "Participaciones en candidaturas"
