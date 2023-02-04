# -*- coding: utf-8 -*-
# Generated by Django 4.1.6 on 2023-02-04 11:47

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
                        to="world.adm0",
                    ),
                ),
                (
                    "adm1",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="world.adm1",
                    ),
                ),
                (
                    "adm2",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="world.adm2",
                    ),
                ),
                (
                    "adm3",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="world.adm3",
                    ),
                ),
                (
                    "adm4",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="world.adm4",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]