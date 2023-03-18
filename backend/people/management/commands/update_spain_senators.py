# -*- coding: utf-8 -*-
import re
import logging
from bs4 import BeautifulSoup
from datetime import date
from django.core.management.base import BaseCommand

from core.services.requests import request_page
from people.services.people_id import people_id_from_name
from people.services.names import clean_spanish_name
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
    Get or update spanish senators from the index of the senate page.
    The following data are obtained:

    Person:
    - first_name, last_name, full_name and id_name
    - metadata    # Updated

    Position:
    - person
    - institution
    - metadata    # Updated
    """

    help = "Update Spain senators"
    search_url = "https://www.senado.es/web/composicionorganizacion/senadores/composicionsenado/senadoresdesde1977/consultaorden/index.html"
    search_data = {
        "legis": "99",  # todas
        "order": "A",
        "boton_obtener_listado": "OBTENER LISTADO",
    }
    sleep_time = 0.5

    def add_arguments(self, parser):
        parser.add_argument(
            "-p", "--period", type=int, nargs="?", help="Period number", default=None
        )

    def get_periods(self, *args, **options):
        spain_congress = Institution.objects.get(name="Senado de España")

        periods = Period.objects.filter(institution=spain_congress)
        if options["period"]:
            periods = periods.filter(number=options["period"])

        return periods.order_by("-number")

    def handle(self, *args, **options):
        for period in self.get_periods(*args, **options):
            if options["verbosity"] >= 2:
                logger.info(f"Updating senators from {period.name}...")

            self.search_data["legis"] = str(period.number)
            response = request_page(self.search_url, self.search_data)
            soup = BeautifulSoup(response, "html.parser")

            for row in soup.select(".caja12-2 .lista-alterna.listaOriginal li"):
                # Person
                metadata = {}
                link = row.select("a")[0]
                name_split = link.text.split(", ")
                full_name = clean_spanish_name(
                    f"{name_split[1]} {name_split[0]}".strip().title()
                )
                id_name = people_id_from_name(full_name)
                person_id = re.search(r"id1=(\d+)$", link["href"])
                metadata["link"] = "https://www.senado.es" + link["href"]
                metadata["person_id"] = person_id.group(1)
                sgroup = row.select("abbr")[0]
                metadata["group_code"] = sgroup.text.strip()
                metadata["group_name"] = sgroup["title"].strip()
                metadata["nombre"] = name_split[1].strip()
                metadata["apellidos"] = name_split[0].strip()

                xml = row.select(".col-5")[1].select("a")
                if xml:
                    metadata["xml_data"] = "https://www.senado.es" + xml[0]["href"]

                person = Person.objects.filter(id_name=id_name).first()
                if not person:
                    person = Person(
                        full_name=full_name,
                        first_name=clean_spanish_name(name_split[1].title()),
                        last_name=clean_spanish_name(name_split[0].title()),
                        id_name=people_id_from_name(full_name),
                        genre="O",
                        metadata={},
                    )
                if not person.metadata.get("www.senado.es"):
                    person.metadata["www.senado.es"] = {}
                person.metadata["www.senado.es"][f"leg-{period.number}"] = metadata
                person.save()

                # Position
                position = Position.objects.filter(person=person, period=period).first()
                if not position:
                    position = Position(
                        period=period,
                        person=person,
                        short_name="Senador",
                        full_name=(
                            f"Senador del {period.institution.name}, {period.name}"
                        ),
                        start=date(2999, 12, 31),  # to be updated later
                        end=date(2999, 12, 31),  # to be updated later
                        metadata={},
                    )
                if not position.metadata.get("www.senado.es"):
                    position.metadata["www.senado.es"] = {}
                position.metadata["www.senado.es"] = metadata
                position.save()

                if options["verbosity"] >= 2:
                    logger.info(f"{person}")

        if options["verbosity"] >= 2:
            logger.info("Done")
