# -*- coding: utf-8 -*-
# Generated by Django 4.1.6 on 2023-04-02 15:07

import core.models.BaseAbstract
import core.storage
import core.validators
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import people.services.staticfiles
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="Identificador único de la instancia del modelo",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Fecha de creación de la instancia"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Última actualización de la instancia"
                    ),
                ),
                (
                    "metadata",
                    models.JSONField(
                        default=core.models.BaseAbstract.json_default_field
                    ),
                ),
                (
                    "full_name",
                    models.CharField(
                        db_index=True,
                        help_text="Nombre completo de la persona",
                        max_length=255,
                    ),
                ),
                (
                    "id_name",
                    models.CharField(
                        db_index=True,
                        help_text="Identificador único del nombre",
                        max_length=255,
                        unique=True,
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True,
                        help_text="Nombre de pila",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, help_text="Apellido/s", max_length=255, null=True
                    ),
                ),
                (
                    "birth_date",
                    models.DateField(
                        blank=True, help_text="Fecha de nacimiento", null=True
                    ),
                ),
                (
                    "birth_date_accuracy",
                    models.IntegerField(
                        blank=True,
                        choices=[(1, "Year"), (2, "Year-Month"), (3, "Year-Month-Day")],
                        help_text="Precisión de la fecha de nacimiento",
                        null=True,
                    ),
                ),
                (
                    "birth_place",
                    django.contrib.gis.db.models.fields.PointField(
                        blank=True,
                        db_index=True,
                        default=None,
                        help_text="Coordenadas del lugar de nacimiento",
                        null=True,
                        srid=4326,
                    ),
                ),
                (
                    "birth_place_name",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        default=None,
                        help_text="Nombre del lugar de nacimiento",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "death_date",
                    models.DateField(
                        blank=True, help_text="Fecha de fallecimiento", null=True
                    ),
                ),
                (
                    "death_date_accuracy",
                    models.IntegerField(
                        blank=True,
                        choices=[(1, "Year"), (2, "Year-Month"), (3, "Year-Month-Day")],
                        help_text="Precisión de la fecha de fallecimiento",
                        null=True,
                    ),
                ),
                (
                    "death_place",
                    django.contrib.gis.db.models.fields.PointField(
                        blank=True,
                        db_index=True,
                        default=None,
                        help_text="Coordenadas del lugar de fallecimiento",
                        null=True,
                        srid=4326,
                    ),
                ),
                (
                    "death_place_name",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        default=None,
                        help_text="Nombre del lugar de fallecimiento",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "genre",
                    models.CharField(
                        choices=[("M", "Hombre"), ("F", "Mujer"), ("O", "Otro")],
                        default=("M", "Hombre"),
                        help_text="Género",
                        max_length=1,
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="Imagen de perfil",
                        null=True,
                        storage=core.storage.FileSystemOverwriteStorage(),
                        upload_to=people.services.staticfiles.person_profile_image_path,
                    ),
                ),
            ],
            options={
                "verbose_name": "Persona",
                "verbose_name_plural": "Personas",
                "db_table": "people_person",
                "ordering": ("id",),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="DeathDateSource",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="Identificador único de la instancia del modelo",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Fecha de creación de la instancia"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Última actualización de la instancia"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True, help_text="Dominio de la fuente", max_length=255
                    ),
                ),
                ("url", models.TextField(help_text="Url completa de la fuente")),
                (
                    "value",
                    models.CharField(
                        help_text="Fecha en crudo. Formato YYYY o YYYY-MM o YYYY-MM-DD",
                        max_length=10,
                        validators=[core.validators.validate_partial_date],
                    ),
                ),
                ("date", models.DateField(help_text="Fecha formateada")),
                (
                    "accuracy",
                    models.IntegerField(
                        choices=[(1, "Year"), (2, "Year-Month"), (3, "Year-Month-Day")],
                        help_text="Precisión de la fecha",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        help_text="Persona a la que pertenece la biografía",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="people.person",
                    ),
                ),
            ],
            options={
                "verbose_name": "Fecha de fallecimiento",
                "verbose_name_plural": "Fechas de fallecimiento",
                "db_table": "people_deathdatesource",
                "ordering": ("id",),
                "abstract": False,
                "unique_together": {("person", "url")},
            },
        ),
        migrations.CreateModel(
            name="BirthPlaceSource",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="Identificador único de la instancia del modelo",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Fecha de creación de la instancia"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Última actualización de la instancia"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True, help_text="Dominio de la fuente", max_length=255
                    ),
                ),
                ("url", models.TextField(help_text="Url completa de la fuente")),
                (
                    "value",
                    models.CharField(
                        help_text="Nombre de la localización", max_length=200
                    ),
                ),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(
                        db_index=True,
                        default=None,
                        help_text="Coordenadas de la localización",
                        null=True,
                        srid=4326,
                    ),
                ),
                (
                    "location_hash",
                    models.CharField(
                        db_index=True,
                        help_text="Hash de las coordenadas de la localización",
                        max_length=16,
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        help_text="Persona a la que pertenece la biografía",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="people.person",
                    ),
                ),
            ],
            options={
                "verbose_name": "Lugar de nacimiento",
                "verbose_name_plural": "Lugares de nacimiento",
                "db_table": "people_birthplacesource",
                "ordering": ("id",),
                "abstract": False,
                "unique_together": {("person", "url")},
            },
        ),
        migrations.CreateModel(
            name="BirthDateSource",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="Identificador único de la instancia del modelo",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Fecha de creación de la instancia"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Última actualización de la instancia"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True, help_text="Dominio de la fuente", max_length=255
                    ),
                ),
                ("url", models.TextField(help_text="Url completa de la fuente")),
                (
                    "value",
                    models.CharField(
                        help_text="Fecha en crudo. Formato YYYY o YYYY-MM o YYYY-MM-DD",
                        max_length=10,
                        validators=[core.validators.validate_partial_date],
                    ),
                ),
                ("date", models.DateField(help_text="Fecha formateada")),
                (
                    "accuracy",
                    models.IntegerField(
                        choices=[(1, "Year"), (2, "Year-Month"), (3, "Year-Month-Day")],
                        help_text="Precisión de la fecha",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        help_text="Persona a la que pertenece la biografía",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="people.person",
                    ),
                ),
            ],
            options={
                "verbose_name": "Fecha de nacimiento",
                "verbose_name_plural": "Fechas de nacimiento",
                "db_table": "people_birthdatesource",
                "ordering": ("id",),
                "abstract": False,
                "unique_together": {("person", "url")},
            },
        ),
        migrations.CreateModel(
            name="BiographySource",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="Identificador único de la instancia del modelo",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Fecha de creación de la instancia"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Última actualización de la instancia"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True, help_text="Dominio de la fuente", max_length=255
                    ),
                ),
                ("url", models.TextField(help_text="Url completa de la fuente")),
                ("value", models.TextField(help_text="Biografía")),
                (
                    "person",
                    models.ForeignKey(
                        help_text="Persona a la que pertenece la biografía",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="people.person",
                    ),
                ),
            ],
            options={
                "verbose_name": "Biografía",
                "verbose_name_plural": "Biografías",
                "db_table": "people_biographysource",
                "ordering": ("id",),
                "abstract": False,
                "unique_together": {("person", "url")},
            },
        ),
    ]
