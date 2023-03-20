# -*- coding: utf-8 -*-
from django.contrib.gis.db import models

from core.models import BaseAbstractModel
from core.storage import FileSystemOverwriteStorage
from people.services.people_id import people_id_from_name
from people.services.staticfiles import person_profile_image_path


class Person(BaseAbstractModel):
    """
    Persona física
    """

    DATE_ACCURACY = (
        (1, "Year"),
        (2, "Year-Month"),
        (3, "Year-Month-Day"),
    )
    GENRES = (
        ("M", "Hombre"),
        ("F", "Mujer"),
        ("O", "Otro"),
    )
    full_name = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Nombre completo de la persona",
    )
    id_name = models.CharField(
        max_length=255,
        db_index=True,
        unique=True,
        help_text="Identificador único del nombre",
    )
    first_name = models.CharField(
        max_length=255,
        help_text="Nombre de pila",
    )
    last_name = models.CharField(
        max_length=255,
        help_text="Apellido/s",
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha de nacimiento",
    )
    birth_date_accuracy = models.IntegerField(
        null=True,
        blank=True,
        choices=DATE_ACCURACY,
        help_text="Precisión de la fecha de nacimiento",
    )
    birth_place = models.PointField(
        null=True,
        blank=True,
        default=None,
        db_index=True,
        help_text="Coordenadas del lugar de nacimiento",
    )
    birth_place_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default=None,
        db_index=True,
        help_text="Nombre del lugar de nacimiento",
    )
    death_date = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha de fallecimiento",
    )
    death_date_accuracy = models.IntegerField(
        null=True,
        blank=True,
        choices=DATE_ACCURACY,
        help_text="Precisión de la fecha de fallecimiento",
    )
    death_place = models.PointField(
        null=True,
        blank=True,
        default=None,
        db_index=True,
        help_text="Coordenadas del lugar de fallecimiento",
    )
    death_place_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default=None,
        db_index=True,
        help_text="Nombre del lugar de fallecimiento",
    )
    genre = models.CharField(
        choices=GENRES,
        max_length=1,
        default=GENRES[0],
        help_text="Género",
    )
    image = models.ImageField(
        upload_to=person_profile_image_path,
        null=True,
        blank=True,
        storage=FileSystemOverwriteStorage(),
        help_text="Imagen de perfil",
    )

    def save(self, *args, **kwargs):
        self.id_name = people_id_from_name(self.full_name)
        super(Person, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name

    class Meta(BaseAbstractModel.Meta):
        db_table = "people_person"
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
