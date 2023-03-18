# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstractModel


class Institution(BaseAbstractModel):
    """
    Institución (congreso, senado, parlamento autonómico...)
    """

    name = models.CharField(
        max_length=250,
        unique=True,
        db_index=True,
        help_text="Nombre formal de la institución",
    )
    adm0 = models.ForeignKey(
        "world.Adm0",
        null=True,
        on_delete=models.PROTECT,
        related_name="institutions",
        help_text="Adm0 (país) al que pertenece la institución",
    )
    adm1 = models.ForeignKey(
        "world.Adm1",
        null=True,
        on_delete=models.PROTECT,
        related_name="institutions",
        help_text="Adm1 (ccaa) al que pertenece la institución",
    )
    adm2 = models.ForeignKey(
        "world.Adm2",
        null=True,
        on_delete=models.PROTECT,
        related_name="institutions",
        help_text="Adm2 (provincia) al que pertenece la institución",
    )
    adm3 = models.ForeignKey(
        "world.Adm3",
        null=True,
        on_delete=models.PROTECT,
        related_name="institutions",
        help_text="Adm3 (región) al que pertenece la institución",
    )
    adm4 = models.ForeignKey(
        "world.Adm4",
        null=True,
        on_delete=models.PROTECT,
        related_name="institutions",
        help_text="Adm4 (municipio) al que pertenece la institución",
    )

    def __str__(self):
        return self.name

    class Meta(BaseAbstractModel.Meta):
        db_table = "positions_institution"
        verbose_name = "Institución"
        verbose_name_plural = "Instituciones"
