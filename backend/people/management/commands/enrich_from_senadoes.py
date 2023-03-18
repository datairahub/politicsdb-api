# -*- coding: utf-8 -*-
import os
import re
import time
import logging
from bs4 import BeautifulSoup
from unidecode import unidecode
from tempfile import NamedTemporaryFile
from urllib.error import HTTPError
from datetime import date, datetime
from django.core.management.base import BaseCommand

from core.services.requests import request_page
from people.services.biographies import register_biography_source
from positions.models import (
    Institution,
    Period,
    Position,
)

logger = logging.getLogger("commands")


class Command(BaseCommand):
    """
    Enrich spanish senators data using the detail page of
    each senator. The following data are obtained:

    Person:
    - image      # Updated
    - biography  # Updated

    Position:
    - start      # Updated
    - end        # Updated
    """

    help = "Enrich Spain senators data with detailed info"
    sleep_time = 0.5

    def add_arguments(self, parser):
        parser.add_argument(
            "-p", "--period", type=int, nargs="?", help="Period number", default=None
        )
        parser.add_argument(
            "--override",
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help="If previous data should be overrided",
        )

    def get_periods(self, *args, **options):
        spain_congress = Institution.objects.get(name="Senado de España")

        periods = Period.objects.filter(institution=spain_congress)
        if options["period"]:
            periods = periods.filter(number=options["period"])

        return periods.order_by("-number")

    def handle(self, *args, **options):
        last_period = (
            Period.objects.filter(institution__name="Senado de España")
            .order_by("number")
            .last()
        )

        for period in self.get_periods(*args, **options):
            for position in Position.objects.filter(period=period):

                if not position.metadata.get("www.senado.es"):
                    continue

                if not position.metadata["www.senado.es"].get("link"):
                    continue

                start, end = self.dates_special_cases(position, *args, **options)

                if not start:
                    url = position.metadata["www.senado.es"]["link"] + "&id2=g"
                    time.sleep(self.sleep_time)

                    try:
                        response = request_page(url).decode("utf-8")
                    except HTTPError:
                        continue

                    if not response:
                        continue

                    soup = BeautifulSoup(response, "html.parser")

                # Fecha alta
                if start:
                    position.start = start
                else:
                    info = soup.select(".caja5-4")[0]
                    info_text = unidecode(info.text.lower())
                    search = re.search(r"fecha: (\d{2}/\d{2}/\d{4})", info_text)
                    search = search.group(1)
                    position.start = datetime.strptime(search, "%d/%m/%Y").date()

                # Fecha baja
                if end:
                    position.end = end
                elif position.period == last_period:
                    position.end = date(2999, 12, 31)
                else:
                    search = re.search(r"baja \((.+?): (\d{2}/\d{2}/\d{4})", info_text)
                    search = search.group(2)
                    position.end = datetime.strptime(search, "%d/%m/%Y").date()

                # Image
                img = soup.select("img.imgSenador")
                if img and not position.person.image:
                    try:
                        img_temp = NamedTemporaryFile(delete=True)
                        img_temp.write(request_page(img[0]["src"]))
                        img_temp.flush()
                        position.person.image.save(
                            os.path.basename(img[0]["src"]), img_temp
                        )
                    except Exception:
                        pass

                # Biography
                bio = soup.select(".caja12-4 .caja5-4 .lista-alterna")
                if bio:
                    register_biography_source(
                        person=position.person,
                        url=url,
                        value=bio[0].text,
                    )

                position.save()

                if options["verbosity"] >= 2:
                    logger.info(f"{position.person}")

        if options["verbosity"] >= 2:
            logger.info("Done")

    def dates_special_cases(self, position, *args, **options):
        """
        Special cases that the shitty senado.es does not handle
        """
        if (
            position.person.id_name == "jose_montilla_aguilera"
            and position.period.number == 13
        ):
            return date(2019, 5, 21), date(2019, 9, 24)

        if (
            position.person.id_name == "arseni_gibert_bosch"
            and position.period.number == 7
        ):
            return date(2000, 3, 12), date(2004, 2, 11)

        if (
            position.person.id_name == "andres_cuevas_gonzalez"
            and position.period.number == 5
        ):
            return date(1993, 6, 29), date(1996, 1, 9)

        if (
            position.person.id_name == "jose_luis_alvarez_emparanza"
            and position.period.number == 3
        ):
            return date(1986, 6, 22), date(1986, 6, 22)

        return None, None
