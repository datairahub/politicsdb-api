# -*- coding: utf-8 -*-
# Generated by Django 4.1.6 on 2023-03-02 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("world", "0005_fill_spain_adm3_adm4"),
    ]

    operations = [
        migrations.AddField(
            model_name="adm0",
            name="flag",
            field=models.ImageField(blank=True, null=True, upload_to="images/adm0/"),
        ),
    ]
