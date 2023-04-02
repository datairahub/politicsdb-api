# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstractModel


class Candidacy(BaseAbstractModel):
    """
    Candidatura
    """

    name = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Nombre completo de la candidatura",
    )
    short_name = models.CharField(
        max_length=255,
        db_index=True,
        null=True,
        blank=True,
        default=None,
        help_text="Siglas de la candidatura",
    )
    period = models.ForeignKey(
        "positions.Period",
        on_delete=models.CASCADE,
        related_name="candidatures",
        help_text="Periodo al cual se presenta la candidatura",
    )
    political_space = models.ForeignKey(
        "organizations.PoliticalSpace",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="candidatures",
        help_text="Espacio político al que pertenece la candidatura",
    )
    source = models.URLField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Fuente de la candidatura",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("id",)
        db_table = "organizations_candidacy"
        verbose_name = "Candidatura"
        verbose_name_plural = "Candidaturas"
        unique_together = (
            (
                "name",
                "period",
            ),
            (
                "short_name",
                "period",
            ),
        )
