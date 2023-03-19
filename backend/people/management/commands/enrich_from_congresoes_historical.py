# -*- coding: utf-8 -*-
import re
import json
import string
import logging
from bs4 import BeautifulSoup
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand

from core.services.requests import request_page
from people.services.people_id import people_id_from_name
from people.services.names import clean_spanish_name
from people.services.birth_dates import register_birth_date_source
from people.models import Person

logger = logging.getLogger("commands")


INCORRECT_PERSONS_MATCH = [
    # People who are marked as correct
    # but they are an incorrect match
    "pedro_fernandez_hernandez",
]


class Command(BaseCommand):
    """
    Enrich spain deputies data from congreso.es historical
    archive. The following data are obtained:

    Person:
    - birth_date
    """

    help = "Enrich spain deputies data from congreso.es historical archive"
    headers = settings.SCRAPERS["congreso_headers"]

    def handle(self, *args, **options):
        names = self.get_historical_legislators_names()

        for person in Person.objects.filter(birth_date=None):
            if person.id_name in INCORRECT_PERSONS_MATCH:
                continue

            if not names.get(person.id_name):
                continue

            result = self.get_historical_data(names.get(person.id_name))

            if not result:
                continue

            for key in result:
                if not key.startswith("elecciones"):
                    continue
                if not result[key].get("enlace"):
                    continue
                if not result[key].get("nume"):
                    continue

                page, url = self.get_historical_detail_page(result[key]["nume"])
                birth_date = self.get_birth_date_from_detail_page(page)

                if not birth_date:
                    continue

                register_birth_date_source(
                    person=person,
                    url=url,
                    value=birth_date,
                )

                if options["verbosity"] >= 2:
                    logger.info(f"{person}")

                break

        if options["verbosity"] >= 2:
            logger.info("Done")

    def get_birth_date_from_detail_page(self, page) -> str:
        if not page:
            return None
        soup = BeautifulSoup(page, "html.parser")
        body = soup.select(".cuerpo_historico_dip_det")
        if not body:
            return None
        search = re.search(r"nacimiento: (\d{1,2}\.\d{1,2}\.\d{4})", body[0].text)
        if not search:
            return None
        return (
            datetime.strptime(search.group(1), "%d.%m.%Y").date().strftime("%Y-%m-%d")
        )

    def get_historical_detail_page(self, legislatornum):
        url = (
            "https://www.congreso.es/historico-diputados"
            "?p_p_id=historicodiputados"
            "&p_p_lifecycle=0"
            "&p_p_state=normal"
            "&p_p_mode=view"
            "&_historicodiputados_mvcRenderCommandName=mostrarDetalle"
            f"&_historicodiputados_nume={legislatornum}"
        )
        return request_page(url, headers=self.headers), url

    def get_historical_data(self, name):
        url = (
            "https://www.congreso.es/es/historico-diputados"
            "?p_p_id=historicodiputados"
            "&p_p_lifecycle=2"
            "&p_p_state=normal"
            "&p_p_mode=view"
            "&p_p_resource_id=filtrarListado"
            "&p_p_cacheability=cacheLevelPage"
        )
        response = request_page(
            url,
            self.get_historical_search_form_data(name),
            headers=self.headers,
        )
        data = json.loads(response)
        return data.get("diputado_1")

    def get_historical_search_form_data(self, name, page=1):
        return {
            "_historicodiputados_texto": "",
            "_historicodiputados_nombre": name,
            "_historicodiputados_genero": "",
            "_historicodiputados_tituloNobiliario": "",
            "_historicodiputados_eleccionesDesde": "",
            "_historicodiputados_eleccionesHasta": "",
            "_historicodiputados_division": "",
            "_historicodiputados_circDistrito": "",
            "_historicodiputados_circunscripcion": "",
            "_historicodiputados_distrito": "",
            "_historicodiputados_assu": "",
            "_historicodiputados_fraccion": "",
            "_historicodiputados_fechaAltaDesde": "",
            "_historicodiputados_fechaAltaHasta": "",
            "_historicodiputados_fechaBajaDesde": "",
            "_historicodiputados_fechaBajaHasta": "",
            "_historicodiputados_orden": 0,
            "_historicodiputados_paginaActual": str(page),
        }

    def get_historical_legislators_names(self):
        names = {}
        for letter in list(string.ascii_lowercase):
            for name in self.get_historical_names_by_letter(letter):
                full_name = clean_spanish_name(
                    name.split(", ")[1] + " " + name.split(", ")[0]
                )
                names[people_id_from_name(full_name)] = name
        return names

    def get_historical_names_by_letter(self, letter):
        url = (
            "https://www.congreso.es/es/historico-diputados"
            "?p_p_id=historicodiputados"
            "&p_p_lifecycle=2"
            "&p_p_state=normal"
            "&p_p_mode=view"
            "&p_p_resource_id=rellenaModalNombre"
            "&p_p_cacheability=cacheLevelPage"
        )
        response = request_page(
            url,
            self.get_historical_modal_names_form_data(letter),
            headers=self.headers,
        )
        return json.loads(response)["popupNombres"]

    def get_historical_modal_names_form_data(self, letter):
        return {
            "_historicodiputados_letra": letter,  # a-z
        }
