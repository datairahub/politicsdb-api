# -*- coding: utf-8 -*-
# Generated by Django 4.1.6 on 2023-02-04 10:59

import core.models
from django.db import migrations, models
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
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("metadata", models.JSONField(default=core.models.json_default_field)),
                ("full_name", models.CharField(db_index=True, max_length=250)),
                (
                    "id_name",
                    models.CharField(db_index=True, max_length=250, unique=True),
                ),
                ("birth_date", models.DateField(blank=True, null=True)),
                (
                    "genre",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")],
                        default=("M", "Male"),
                        max_length=1,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
