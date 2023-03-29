# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstractModel
from core.validators import validate_hex_color


class Party(BaseAbstractModel):
    """
    Partido político
    """

    LEVELS = (
        ("adm0", "Estatal"),
        ("adm1", "CCAA"),
        ("adm2", "Provincial"),
        ("adm3", "Regional"),
        ("adm4", "Municipal"),
        ("adm5", "Sub-municipal"),
    )
    name = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Nombre completo del partido político",
    )
    short_name = models.CharField(
        max_length=255,
        db_index=True,
        null=True,
        blank=True,
        default=None,
        help_text="Siglas del partido político",
    )
    code = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Código único de registro. Números mayores de 100000 son no existentes",
    )
    color = models.CharField(
        max_length=7,
        help_text="Color principal del partido político",
        default="#000000",
        validators=[validate_hex_color],
    )
    adm0 = models.ForeignKey(
        "world.Adm0",
        null=True,
        on_delete=models.PROTECT,
        related_name="parties",
        help_text="País al que pertenece el partido político",
    )
    level = models.CharField(
        max_length=4,
        choices=LEVELS,
        default=LEVELS[0][0],
        help_text="Ámbito (estatal, municipal...)",
    )
    founded = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha de creación del partido",
    )
    start = models.DateField(
        help_text="Fecha de registro del partido",
    )
    end = models.DateField(
        help_text="Fecha de disolución del partido",
    )
    address = models.TextField(
        null=True,
        blank=True,
        help_text="Domicilio social del partido",
    )
    email = models.EmailField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Email del partido",
    )
    web = models.URLField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Página web del partido",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("id",)
        db_table = "organizations_party"
        verbose_name = "Partido"
        verbose_name_plural = "Partidos"
        unique_together = (("name", "adm0"),)
