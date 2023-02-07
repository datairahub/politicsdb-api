# -*- coding: utf-8 -*-
# Generated by Django 4.1.6 on 2023-02-07 20:30

import core.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0002_fill_spain_goverment_persons"),
    ]

    operations = [
        migrations.CreateModel(
            name="BiographySource",
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
                ("url", models.TextField()),
                ("bio", models.TextField()),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="biographysources",
                        to="people.person",
                    ),
                ),
            ],
            options={
                "unique_together": {("person", "url")},
            },
        ),
    ]
