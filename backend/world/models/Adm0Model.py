# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstractModel
from core.storage import FileSystemOverwriteStorage
from world.services.staticfiles import (
    adm_flag_path,
    validate_flag_filetype,
)


class Adm0(BaseAbstractModel):
    """
    Country
    """

    name = models.CharField(max_length=100, db_index=True, help_text="Nombre completo")
    iso_name = models.CharField(
        max_length=100, db_index=True, help_text="Nombre según ISO-3166"
    )
    code = models.CharField(
        max_length=2,
        db_index=True,
        unique=True,
        help_text="Código Alpha-2 según ISO-3166-1",
    )
    flag = models.ImageField(
        upload_to=adm_flag_path,
        null=True,
        blank=True,
        validators=[validate_flag_filetype],
        storage=FileSystemOverwriteStorage(),
        help_text="Bandera o representación",
    )

    def __str__(self):
        return f"{self.name} ({self.iso_name})"

    class Meta(BaseAbstractModel.Meta):
        verbose_name = "Adm0"
        verbose_name_plural = "Adm0"
