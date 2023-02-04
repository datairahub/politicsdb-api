# -*- coding: utf-8 -*-
# Generated by Django 4.1.6 on 2023-02-04 13:53

import core.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("persons", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BirthSource",
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
                ("is_exact", models.BooleanField(default=False)),
                ("date", models.DateField(default=django.utils.timezone.now)),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="persons.person"
                    ),
                ),
            ],
            options={
                "unique_together": {("person", "url")},
            },
        ),
    ]
