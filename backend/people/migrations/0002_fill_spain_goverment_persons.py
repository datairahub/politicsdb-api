# -*- coding: utf-8 -*-
import csv
from django.db import migrations
from django.conf import settings
from people.models import Person
from people.services.people_id import people_id_from_name
from people.services.names import clean_spanish_name
from people.services.birth_dates import register_birth_date_source

DATA_DIR = settings.BASE_DIR.parent / "data_input" / "birth_dates"
FILENAME = "es_governors.csv"


def apply_migration(apps, schema_editor):
    with open(DATA_DIR / FILENAME, "r") as f:
        csv_reader = csv.DictReader(f, delimiter=",")

        for row in csv_reader:
            full_name = clean_spanish_name(f"{row['first_name']} {row['last_name']}")
            person = Person.objects.create(
                full_name=full_name,
                id_name=people_id_from_name(full_name),
                first_name=clean_spanish_name(row["first_name"]),
                last_name=clean_spanish_name(row["last_name"]),
                genre=row["genre"],
            )
            register_birth_date_source(
                person=person,
                url=row["source"],
                value=row["birth_date"],
            )


def revert_migration(apps, schema_editor):
    Person = apps.get_model("people", "Person")
    BirthDateSource = apps.get_model("people", "BirthDateSource")
    Person.objects.all().delete()
    BirthDateSource.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration),
    ]
