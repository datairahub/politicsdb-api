# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstractModel


class PoliticalSpace(BaseAbstractModel):
    """
    Espacio político (agrupación de candidaturas a lo largo del tiempo)
    """

    name = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Nombre del espacio",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("id",)
        db_table = "organizations_politicalspace"
        verbose_name = "Espacio político"
        verbose_name_plural = "Espacios políticos"
