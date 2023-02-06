# -*- coding: utf-8 -*-
# Generated by Django 4.1.6 on 2023-02-06 16:45

import core.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("organizations", "0001_initial"),
        ("world", "0005_fill_spain_adm3_adm4"),
        ("people", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Institution",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("metadata", models.JSONField(default=core.models.json_default_field)),
                ("name", models.CharField(db_index=True, max_length=250, unique=True)),
                (
                    "adm0",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="institutions",
                        to="world.adm0",
                    ),
                ),
                (
                    "adm1",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="institutions",
                        to="world.adm1",
                    ),
                ),
                (
                    "adm2",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="institutions",
                        to="world.adm2",
                    ),
                ),
                (
                    "adm3",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="institutions",
                        to="world.adm3",
                    ),
                ),
                (
                    "adm4",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="institutions",
                        to="world.adm4",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Period",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("metadata", models.JSONField(default=core.models.json_default_field)),
                ("name", models.CharField(db_index=True, max_length=250)),
                ("number", models.IntegerField()),
                ("code", models.CharField(db_index=True, max_length=250)),
                ("start", models.DateField()),
                ("end", models.DateField()),
                (
                    "institution",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="periods",
                        to="positions.institution",
                    ),
                ),
            ],
            options={
                "unique_together": {
                    ("number", "institution"),
                    ("name", "institution"),
                    ("code", "institution"),
                },
            },
        ),
        migrations.CreateModel(
            name="Position",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("metadata", models.JSONField(default=core.models.json_default_field)),
                ("short_name", models.CharField(max_length=255)),
                ("full_name", models.TextField()),
                ("start", models.DateField()),
                ("end", models.DateField()),
                (
                    "period",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="positions",
                        to="positions.period",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="positions",
                        to="people.person",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PositionParty",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("metadata", models.JSONField(default=core.models.json_default_field)),
                ("start", models.DateField()),
                ("end", models.DateField()),
                (
                    "party",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="positionparties",
                        to="organizations.party",
                    ),
                ),
                (
                    "position",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="positionparties",
                        to="positions.position",
                    ),
                ),
            ],
            options={
                "unique_together": {("position", "party")},
            },
        ),
    ]
