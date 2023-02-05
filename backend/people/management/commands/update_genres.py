# -*- coding: utf-8 -*-
import os
import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from world.models import Adm0
from people.models import Person

logger = logging.getLogger("commands")


class Command(BaseCommand):
    """
    Actualizar el género utilizando el primer nombre
    y archivos de nombre/género de data_input/genres
    """

    help = "Update people genres"
    genres_folder = settings.BASE_DIR.parent / "data_input" / "genres"

    def handle(self, *args, **options):
        self.names = self.get_genre_names_from_files()

        for adm0 in Adm0.objects.all():
            if options["verbosity"] >= 2:
                logger.info(f"Updating names for country {adm0.name}...")
            for person in Person.objects.filter(
                positions__period__institution__adm0=adm0
            ).distinct():
                self.update_person_genre(person, adm0.code, *args, **options)

        if options["verbosity"] >= 2:
            logger.info("Done")

    def update_person_genre(self, person, country_code, *args, **options):
        first_name = person.full_name.split(" ")[0].lower()

        if first_name in self.names[country_code]["female"]:
            person.genre = "F"
        elif first_name in self.names[country_code]["male"]:
            person.genre = "M"
        else:
            raise Exception(f'Genre for "{first_name}" not found ({person.full_name})')

        person.save(update_fields=["genre"])
        if options["verbosity"] >= 2:
            logger.info(f"{person} genre updated ({person.genre})")

    def get_genre_names_from_files(self):
        country_names = {}
        for filename in os.listdir(self.genres_folder):
            country = filename.split("_")[0]
            genre = filename.split("_")[1].split(".")[0]

            if not country in country_names:
                country_names[country] = {
                    "male": [],
                    "female": [],
                }

            with open(os.path.join(self.genres_folder, filename), "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    country_names[country][genre].append(line.strip())

        return country_names
