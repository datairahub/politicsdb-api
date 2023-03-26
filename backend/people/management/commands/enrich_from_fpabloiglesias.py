# -*- coding: utf-8 -*-
import sys
import time
import logging
from bs4 import BeautifulSoup
from unidecode import unidecode
from django.conf import settings
from django.core.management.base import BaseCommand
from core.services.requests import request_page

sys.path.append(str(settings.BASE_DIR.parent))
from parsers.fpabloiglesias import FPabloIglesiasParser
from people.services.biographies import register_biography_source
from people.services.birth_dates import register_birth_date_source
from people.models import Person

logger = logging.getLogger("commands")

INCORRECT_TITLES = [
    # Titles parts for generic pages that
    # do not correspond to any person
    "Letra Internacional",
    "Cartas de Ginebra",
    "elecciones",
    "Izquierdas",
    "Congreso",
    "Colaboradores",
    "Fusilamiento",
    "Internacional",
    "Equipo de",
    "Constitución",
    "Resultados",
    "Historia de la Fundación",
    "Transición y democracia",
    "Hablamos de Europa",
    "Archivo y biblioteca",
    "Del Socialismo exiliado",
    "El nacimiento de la política",
    "Archivo y biblioteca",
    "Presentación Retos",
]

CORRECT_PERSONS_MISMATCH = [
    # People who are marked as incorrect when comparing
    # person.last_name with a profile pares.mcu.es page title
    # but they are a correct match
    "antonio_bisbal_iborra",
    "julian_chia_gutierrez",
    "jaime_ribas_prats",
    "felip_lorda_alaiz",
    "jaime_gaspar_auria",
    "salvador_moragues_berto",
    "francisco_parras_collado",
    "manuel_lucio_diaz_marta_pinilla",
    "teresa_cunillera_mestres",
    "rosa_barenys_martorell",
    "felipe_guillermo_guardiola_selles",
    "alfonso_arenas_ferriz",
    "maria_dolores_renau_manen",
    "angel_franco_gutiez",
    "marta_angela_mata_garriga",
    "marta_mata_garriga",
    "jose_valentin_anton",
    "andres_eguibar_rivas",
    "matias_camacho_lloriz",
    "antonio_jara_andreu",
    "angel_martinez_sanjuan",
    "ana_isabel_arnaiz_las_revillas_garcia",
    "gerard_alvarez_garcia",
    "miguel_castells_arteche",
    "alfons_cuco_giner",
    "francisco_gonzalez_amadios",
]

INCORRECT_PERSONS_MISMATCH = [
    # People who are marked as correct when comparing
    # person.last_name with a profile pares.mcu.es page title
    # but they are an incorrect match
    "jose_latorre_ruiz",
    "andres_lorite_lorite",
    "gerard_alvarez_garcia",
    "leopoldo_herrero_ruiz",
]


class Command(BaseCommand):
    """
    Enriquecer con datos de la página fpabloiglesias.es
    Datos a obtener:
        - Descripción
        - Posición
        - Fecha de nacimiento
        - Imágenes (urls)
    """

    help = "Update birth dates using fpabloiglesias.es"
    sleep_time = 0
    domain = "https://fpabloiglesias.es"

    def handle(self, *args, **options):
        self.update_birth_dates_from_paresmcues(*args, **options)
        if options["verbosity"] >= 2:
            logger.info("Done")

    def update_birth_dates_from_paresmcues(self, *args, **options):
        for person in Person.objects.filter(
            positions__period__institution__adm0__code="es"
        ).distinct():

            if not person.last_name:
                # last_name is used to verify that the match is correct
                continue

            if person.id_name in INCORRECT_PERSONS_MISMATCH:
                # person is an incorrect match
                continue

            if person.metadata.get("fpabloiglesias.es") and person.metadata[
                "fpabloiglesias.es"
            ].get("link"):
                # If person is already enriched, continue
                continue

            time.sleep(self.sleep_time)

            # Get search page
            name = unidecode(person.full_name).strip().replace(" ", "+")
            url = self.domain + (f"/?s={name}")
            response = request_page(url).decode("utf-8")
            soup = BeautifulSoup(response, "html.parser")
            articles = soup.select(".x-main article")

            if not (articles and len(articles) == 1):
                # 0 or more than 1 result -> imprecise search
                continue

            if articles[0]["id"] == "post-0":
                # 'Nothing found' box
                continue

            # Get profile page
            profile_url = articles[0].select(".entry-title a")[0]["href"]
            page = request_page(profile_url).decode("utf-8")
            parser = FPabloIglesiasParser(page)

            if not parser.is_parsed:
                continue

            if (not parser.title) or any(
                [inc_title in parser.title for inc_title in INCORRECT_TITLES]
            ):
                continue

            if (not person.last_name.lower() in parser.title.lower()) and (
                not person.id_name in CORRECT_PERSONS_MISMATCH
            ):
                # Person page title doesn't contain the person last name -> imprecise match
                continue

            # store common data in person metadata
            if not person.metadata.get("fpabloiglesias.es"):
                person.metadata["fpabloiglesias.es"] = {}

            person.metadata["fpabloiglesias.es"]["link"] = profile_url
            person.metadata["fpabloiglesias.es"]["title"] = parser.title
            person.metadata["fpabloiglesias.es"]["imgs"] = parser.images
            person.metadata["fpabloiglesias.es"]["position"] = parser.position
            person.metadata["fpabloiglesias.es"]["birth_date"] = parser.birth_date_str

            if parser.description:
                register_biography_source(
                    person=person,
                    url=profile_url,
                    value=parser.description,
                )

            if parser.birth_date:
                register_birth_date_source(
                    person=person,
                    url=profile_url,
                    value=parser.birth_date,
                )

            person.save(update_fields=["metadata"])

            if options["verbosity"] >= 2:
                logger.info(f"{person}")
