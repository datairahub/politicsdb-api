# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime
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
    Obtener miembros del congreso de España desde el índice de
    la página del congreso. Se obtienen los siguientes datos:
        - Nombre completo
        - Género
        - Fecha de alta
        - Fecha de baja
    Los datos raw se guardan en metadata['www.congreso.es']
    """

    help = "Update Spain legislators"
    search_url = "https://www.congreso.es/busqueda-de-diputados?p_p_id=diputadomodule&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=searchDiputados&p_p_cacheability=cacheLevelPage"
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
    headers = {
        "cookie": "GUEST_LANGUAGE_ID=es_ES; COOKIE_SUPPORT=true; JSESSIONID=IUl3YyP_aO-ox9UyGdTnCAbnXBRTALdSd1kwmXry.cgdpjbnode2pro",
        "origin": "https://www.congreso.es",
        "referer": "https://www.congreso.es/busqueda-de-diputados",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    }

    def handle(self, *args, **options):
        spain_congress = Institution.objects.get(name="Parlamento de España")

        for period in Period.objects.filter(institution=spain_congress):
            logger.info(f"Getting legislators from {period.name}...")

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
                        birth_date=None,
                    )

                if not person.metadata.get("www.congreso.es", None):
                    person.metadata["www.congreso.es"] = {}
                person.metadata["www.congreso.es"][
                    f"legislatura-{period.number}"
                ] = member

                person.save()
                logger.info(f"{person} saved")

                # Position
                position = Position.objects.filter(period=period, person=person).first()
                if not position:
                    position = Position(period=period, person=person)
                position.short_name = "Diputado"
                position.full_name = (
                    f"Diputado del {period.institution.name}, {period.name}"
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
                logger.info(f"{position} saved")

        logger.info("Done")

    def get_custom_fix_full_name(self, name):
        names = {
            "Rafael J. Portanet Suárez": "Rafael Jesús Portanet Suárez",
        }
        return names.get(name, name)

    def get_legislature_members(self, number):
        self.search_data["_diputadomodule_idLegislatura"] = str(number)
        response = request_page(self.search_url, self.search_data, self.headers)
        return json.loads(response)["data"]
