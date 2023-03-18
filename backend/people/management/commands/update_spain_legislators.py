# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand

from people.services.people_id import people_id_from_name
from people.services.names import clean_spanish_name
from core.services.requests import request_page
from people.models import (
    Person,
)
from positions.models import (
    Institution,
    Period,
    Position,
)

logger = logging.getLogger("commands")


class Command(BaseCommand):
    """
    Get or update spanish congress members from the
    index of the congress page. The following data are obtained:

    Person:
    - first_name, last_name, full_name and id_name
    - genre
    - metadata    # Updated

    Position:
    - person
    - institution
    - start       # Updated
    - end         # Updated
    - metadata    # Updated
    """

    help = "Update Spain legislators"
    search_url = "https://www.congreso.es/es/busqueda-de-diputados?p_p_id=diputadomodule&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=searchDiputados&p_p_cacheability=cacheLevelPage"
    search_data = {
        "_diputadomodule_idLegislatura": "0",  # -1 for all legislatures
        "_diputadomodule_genero": "0",
        "_diputadomodule_grupo": "all",
        "_diputadomodule_tipo": "2",  # 0 active, 1 inactive, 2 all
        "_diputadomodule_nombre": "",
        "_diputadomodule_apellidos": "",
        "_diputadomodule_formacion": "all",
        "_diputadomodule_filtroProvincias": "[]",
        "_diputadomodule_nombreCircunscripcion": "",
    }
    headers = settings.SCRAPERS["congreso_headers"]

    def add_arguments(self, parser):
        parser.add_argument(
            "-p", "--period", type=int, nargs="?", help="Period number", default=None
        )

    def get_periods(self, *args, **options):
        spain_congress = Institution.objects.get(name="Parlamento de España")

        periods = Period.objects.filter(institution=spain_congress)
        if options["period"]:
            periods = periods.filter(number=options["period"])

        return periods.order_by("-number")

    def handle(self, *args, **options):
        for period in self.get_periods(*args, **options):
            if options["verbosity"] >= 2:
                logger.info(f"Updating legislators from {period.name}...")

            for member in self.get_legislature_members(period.number):
                # Person
                full_name = self.get_custom_fix_full_name(
                    f"{member['nombre']} {member['apellidos']}"
                )
                full_name = clean_spanish_name(full_name)
                id_name = people_id_from_name(full_name)
                person = Person.objects.filter(id_name=id_name).first()
                if not person:
                    person = Person(
                        full_name=full_name,
                        first_name=clean_spanish_name(member["nombre"]),
                        last_name=clean_spanish_name(member["apellidos"]),
                        id_name=people_id_from_name(full_name),
                        genre="M" if member["genero"] == 1 else "F",
                    )

                if not person.metadata.get("www.congreso.es"):
                    person.metadata["www.congreso.es"] = {}

                person.metadata["www.congreso.es"][f"leg-{period.number}"] = member
                person.save()

                # Position
                position = Position.objects.filter(period=period, person=person).first()

                if not position:
                    position = Position(
                        period=period,
                        person=person,
                        short_name="Diputado",
                        full_name=f"Diputado del {period.institution.name}, {period.name}",
                    )

                position.start = datetime.strptime(member["fchAlta"], "%d/%m/%Y").date()
                if member["fchBaja"]:
                    position.end = datetime.strptime(
                        member["fchBaja"], "%d/%m/%Y"
                    ).date()
                else:
                    position.end = datetime.strptime("31/12/2999", "%d/%m/%Y").date()

                position.metadata["www.congreso.es"] = member
                position.save()

                if options["verbosity"] >= 2:
                    logger.info(f"{person}")

        if options["verbosity"] >= 2:
            logger.info("Done")

    def get_custom_fix_full_name(self, name):
        names = {
            "Rafael J. Portanet Suárez": "Rafael Jesús Portanet Suárez",
        }
        return names.get(name, name)

    def get_legislature_members(self, number):
        self.search_data["_diputadomodule_idLegislatura"] = str(number)
        response = request_page(self.search_url, self.search_data, self.headers)
        data = json.loads(response)["data"]
        if not len(data):
            logger.error(f"No data found for legislature {number}")
        return data
