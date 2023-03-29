# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstractModel


class Foundation(BaseAbstractModel):
    """
    Fundación
    """

    name = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Nombre completo de la fundación",
    )
    start = models.DateField(
        help_text="Fecha de creación de la fundación",
    )
    end = models.DateField(
        help_text="Fecha de disolución de la fundación",
    )
    address = models.TextField(
        null=True,
        blank=True,
        help_text="Domicilio social de la fundación",
    )
    email = models.EmailField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Email de la fundación",
    )
    web = models.URLField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Página web de la fundación",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("id",)
        db_table = "organizations_foundation"
        verbose_name = "Fundación"
        verbose_name_plural = "Fundaciones"
