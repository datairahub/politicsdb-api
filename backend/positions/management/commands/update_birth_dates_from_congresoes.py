# -*- coding: utf-8 -*-
import re
import time
import logging
from datetime import datetime
from django.core.management.base import BaseCommand
from core.services.requests import request_page
from positions.models import Position
from people.models import BirthSource

logger = logging.getLogger("commands")


class Command(BaseCommand):
    """
    Obtener la fecha de nacimiento de los diputados
    usando la página web del congreso
    """

    help = "Update legislators birth dates using congreso.es pages"
    sleep_time = 0
    headers = {
        "cookie": "GUEST_LANGUAGE_ID=es_ES; COOKIE_SUPPORT=true; JSESSIONID=IUl3YyP_aO-ox9UyGdTnCAbnXBRTALdSd1kwmXry.cgdpjbnode2pro",
        "origin": "https://www.congreso.es",
        "referer": "https://www.congreso.es/busqueda-de-diputados",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    }

    def handle(self, *args, **options):
        self.update_spain_legislators_from_congresoes()
        logger.info("Done")

    def update_spain_legislators_from_congresoes(self):
        # birth_date_source, _ = BirthDateSource.objects.get_or_create(name='www.congreso.es')
        for position in Position.objects.filter(
            period__institution__name="Parlamento de España",
            period__number__gte=7,  # conreso.es only has dates from legislature 7 onwards
        ):
            if not position.metadata.get("www.congreso.es"):
                continue

            time.sleep(self.sleep_time)
            birth_date, url = self.get_spain_legislators_date(position)
            if not birth_date:
                continue

            position.person.birth_date = birth_date
            position.person.save(update_fields=["birth_date"])

            if not BirthSource.objects.filter(person=position.person, url=url).exists():
                # birth source not registered yet
                BirthSource(
                    person=position.person,
                    url=url,
                    is_exact=True,
                ).save()

            logger.info(f"{position.person} birth date updated")

    def get_spain_legislators_date(self, position):
        codParlamentario = position.metadata["www.congreso.es"]["codParlamentario"]
        url = (
            "https://www.congreso.es/busqueda-de-diputados?"
            "p_p_id=diputadomodule"
            "&p_p_lifecycle=0"
            "&p_p_state=normal"
            "&p_p_mode=view"
            "&_diputadomodule_mostrarFicha=true"
            f"&codParlamentario={codParlamentario}"
            f"&idLegislatura={position.period.code}"
            "&mostrarAgenda=false"
        )
        response = request_page(url, headers=self.headers).decode("utf-8")

        birth_match = re.search(
            r"Nacid[a|o] el (\w{3}) (\w{3}) (\d{1,2}) 00:00:00 \w{1,4} (\d{4})",
            response,
        )
        if birth_match:
            # Nacido el Wed Apr 14 00:00:00 CEST 1976
            # Nacido el Thu May 21 00:00:00 CET 1970
            str_date = f"{birth_match.group(3)}-{self.named_month_to_number(birth_match.group(2).lower())}-{birth_match.group(4)}"
            return datetime.strptime(str_date, "%d-%m-%Y").date(), url

        return None, None

    def named_month_to_number(self, month):
        """
        Convert string month to ordinal
        """
        # fmt: off
        months = {
            "enero":      '01',
            "ene":        '01',
            "january":    '01',
            "jan":        '01',
            "febrero":    '02',
            "feb":        '02',
            "february":   '02',
            "marzo":      '03',
            "mar":        '03',
            "march":      '03',
            "abril":      '04',
            "abr":        '04',
            "april":      '04',
            "apr":        '04',
            "mayo":       '05',
            "may":        '05',
            "junio":      '06',
            "jun":        '06',
            "june":       '06',
            "julio":      '07',
            "jul":        '07',
            "july":       '07',
            "agosto":     '08',
            "ago":        '08',
            "august":     '08',
            "aug":        '08',
            "septiembre": '09',
            "sep":        '09',
            "sept":       '09',
            "september":  '09',
            "octubre":    '10',
            "oct":        '10',
            "october":    '10',
            "noviembre":  '11',
            "nov":        '11',
            "november":   '11',
            "diciembre":  '12',
            "dic":        '12',
            "december":   '12',
            "dec":        '12',
        }
        # fmt: on
        return months.get(month.lower(), month.lower())
