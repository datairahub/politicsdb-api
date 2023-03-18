# -*- coding: utf-8 -*-
import os
import re
import time
import logging
from bs4 import BeautifulSoup
from tempfile import NamedTemporaryFile
from django.conf import settings
from django.core.management.base import BaseCommand
from core.services.requests import request_page
from people.services.birth_dates import register_birth_date_source
from people.services.biographies import register_biography_source
from positions.models import Position

logger = logging.getLogger("commands")


class Command(BaseCommand):
    """
    Obtener datos de cada ficha de diputado de la página web del congreso
    """

    help = "Update legislators data using congreso.es pages"
    base_url = "https://www.congreso.es"
    sleep_time = 0.2
    headers = settings.SCRAPERS["congreso_headers"]

    def handle(self, *args, **options):
        self.update_spain_legislators_from_congresoes(*args, **options)
        if options["verbosity"] >= 2:
            logger.info("Done")

    def update_spain_legislators_from_congresoes(self, *args, **options):
        for position in Position.objects.filter(
            period__institution__name="Parlamento de España",
            period__number__gte=7,  # conreso.es only has dates from legislature 7 onwards
        ):
            if not position.metadata.get("www.congreso.es"):
                continue

            time.sleep(self.sleep_time)
            data = self.get_legislator_detail_data(position)

            if data.get("image"):
                position.person.image.save(
                    os.path.basename(data["image"]["url"]),
                    data["image"]["file"],
                )

            if data.get("birth_date"):
                register_birth_date_source(
                    person=position.person,
                    url=data.get("url"),
                    value=data["birth_date"],
                )

            if data.get("biography"):
                register_biography_source(
                    person=position.person,
                    url=data.get("url"),
                    value=data["biography"],
                )

            position.person.save()
            position.save()

            if options["verbosity"] >= 2:
                logger.info(f"{position.person} updated")

    def get_legislator_detail_data(self, position) -> dict:
        """
        Get spanish legislator detail data
        """
        codParlamentario = position.metadata["www.congreso.es"]["codParlamentario"]
        data = {
            "url": (
                "https://www.congreso.es/busqueda-de-diputados?"
                "p_p_id=diputadomodule"
                "&p_p_lifecycle=0"
                "&p_p_state=normal"
                "&p_p_mode=view"
                "&_diputadomodule_mostrarFicha=true"
                f"&codParlamentario={codParlamentario}"
                f"&idLegislatura={position.period.code}"
                "&mostrarAgenda=false"
            ),
        }
        response = request_page(data["url"], headers=self.headers).decode("utf-8")
        soup = BeautifulSoup(response, "html.parser")

        data["birth_date"] = self.get_birth_date(response)
        data["image"] = self.get_profile_image(soup)
        data["biography"] = self.get_biography(soup)

        return data

    def get_birth_date(self, response) -> str:
        """
        Extract birth date from html response

        Formats:
        - Nacido el Wed Apr 14 00:00:00 CEST 1976
        - Nacido el Thu May 21 00:00:00 CET 1970

        :returns: YYYY-MM-DD date (string)
        """

        birth_match = re.search(
            r"Nacid[a|o] el (\w{3}) (\w{3}) (\d{1,2}) 00:00:00 \w{1,4} (\d{4})",
            response,
        )
        if not birth_match:
            return None

        return f"{birth_match.group(4)}-{self.named_month_to_number(birth_match.group(2).lower())}-{birth_match.group(3)}"

    def get_profile_image(self, soup) -> dict:
        """
        Extract profile image from html response

        :returns: {"url": str, "file": NamedTemporaryFile}
        """

        img = soup.select("img.card-img-top")

        if not img:
            return None

        url = f"{self.base_url}{img[0]['src']}"

        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(request_page(url, headers=self.headers))
        img_temp.flush()

        return {
            "url": url,
            "file": img_temp,
        }

    def get_biography(self, soup) -> str:
        """
        Extract profile biography from html response
        """
        for block in soup.select(".cuerpo-diputado-detalle .col-12"):
            if "Ficha personal" in block.text:
                for tag in soup.select(".f-alta"):
                    tag.decompose()
                text = block.text
                text = text.replace("\n", " ").replace("\t", " ").replace("\r", " ")
                text = text.replace("Ficha personal", "")
                while "  " in text:
                    text = text.replace("  ", " ")
                return text.strip()

        return None

    def named_month_to_number(self, month: str) -> str:
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
