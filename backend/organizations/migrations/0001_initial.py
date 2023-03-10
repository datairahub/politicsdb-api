# -*- coding: utf-8 -*-
# Generated by Django 4.1.6 on 2023-02-04 14:54

import core.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("world", "0005_fill_spain_adm3_adm4"),
    ]

    operations = [
        migrations.CreateModel(
            name="Party",
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
                ("name", models.CharField(db_index=True, max_length=255)),
                ("short_name", models.CharField(db_index=True, max_length=255)),
                ("color", models.CharField(max_length=7)),
                (
                    "adm0",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="parties",
                        to="world.adm0",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Parties",
                "unique_together": {("name", "adm0"), ("short_name", "adm0")},
            },
        ),
    ]
