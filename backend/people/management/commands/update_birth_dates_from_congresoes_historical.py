# -*- coding: utf-8 -*-
import re
import json
import string
import logging
from bs4 import BeautifulSoup
from datetime import datetime
from django.core.management.base import BaseCommand

from core.services.requests import request_page
from people.services.people_id import people_id_from_name
from people.services.names import clean_spanish_name
from people.services.birth_dates import register_birth_date_source
from people.models import Person

logger = logging.getLogger("commands")


class Command(BaseCommand):
    """
    Obtener la fecha de nacimiento de algunos diputados
    cuya fecha no aparece en la página de perfil del congreso
    pero si en la página histórica del congreso
    """

    help = "Update Spain legislators birth dates from congreso.es historial archive"
    headers = {
        "cookie": "GUEST_LANGUAGE_ID=es_ES; COOKIE_SUPPORT=true; JSESSIONID=IUl3YyP_aO-ox9UyGdTnCAbnXBRTALdSd1kwmXry.cgdpjbnode2pro",
        "origin": "https://www.congreso.es",
        "referer": "https://www.congreso.es/busqueda-de-diputados",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    }

    def handle(self, *args, **options):
        self.update_birth_dates_from_congresoes_historical(args, options)
        if options["verbosity"] >= 2:
            logger.info("Done")

    def update_birth_dates_from_congresoes_historical(self, *args, **options):
        names = self.get_historical_legislators_names()

        for person in Person.objects.filter(birth_date=None):
            if not names.get(person.id_name):
                continue

            result = self.get_historical_data(names.get(person.id_name))
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

                # save person birth date
                person.birth_date = birth_date
                person.save(update_fields=["birth_date"])
                register_birth_date_source(person, url, birth_date, True)
                if options["verbosity"] >= 2:
                    logger.info(f"{person} birth date updated")
                break

    def get_birth_date_from_detail_page(self, page):
        if not page:
            return None
        soup = BeautifulSoup(page, "html.parser")
        body = soup.select(".cuerpo_historico_dip_det")
        if not body:
            return None
        search = re.search(r"nacimiento: (\d{1,2}\.\d{1,2}\.\d{4})", body[0].text)
        if not search:
            return None
        return datetime.strptime(search.group(1), "%d.%m.%Y").date()

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
            "https://www.congreso.es/historico-diputados"
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
        return json.loads(response)["diputado_1"]

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
            "https://www.congreso.es/historico-diputados"
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
