# -*- coding: utf-8 -*-
import logging
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from datetime import datetime
from django.core.management.base import BaseCommand

from core.services.requests import request_page
from people.services.birth_dates import register_birth_date_source
from people.services.death_dates import register_death_date_source
from people.services.biographies import register_biography_source
from positions.models import (
    Institution,
    Period,
    Position,
)

logger = logging.getLogger("commands")


class Command(BaseCommand):
    """
    Enrich spanish senators data using each senator
    open data xml file (only a few have it). The following data
    are obtained:

    Person
    - metadata
    - birth_date
    - death_date
    - biography
    """

    help = "Enrich Spain senators data with opendata files"

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
        fetched_persons_id = []

        for period in self.get_periods(*args, **options):
            for position in Position.objects.filter(period=period):

                if not position.metadata["www.senado.es"].get("xml_data", None):
                    # senators without open data
                    continue

                if not options["override"]:
                    if position.metadata["www.senado.es"].get("sexo", None):
                        # senators already fetched
                        continue

                if position.person.id in fetched_persons_id:
                    # senators already fetched in other period (current execution)
                    continue

                url = position.metadata["www.senado.es"]["xml_data"]
                url = url.split(".xml")[0] + ".xml"
                url = url.replace("web/../", "")

                try:
                    response = request_page(url)
                except HTTPError:
                    continue

                if not response:
                    continue

                soup = BeautifulSoup(response, "html.parser")

                if soup.find("sexo") and soup.find("sexo").string:
                    position.person.metadata["www.senado.es"]["sexo"] = soup.find(
                        "sexo"
                    ).string.strip()

                if soup.find("estadocivil") and soup.find("estadocivil").string:
                    position.person.metadata["www.senado.es"][
                        "estadocivil"
                    ] = soup.find("estadocivil").string.strip()

                if soup.find("fechanacimiento") and soup.find("fechanacimiento").string:
                    position.person.metadata["www.senado.es"][
                        "fechanacimiento"
                    ] = soup.find("fechanacimiento").string.strip()

                if soup.find("lugarnacimiento") and soup.find("lugarnacimiento").string:
                    position.person.metadata["www.senado.es"][
                        "lugarnacimiento"
                    ] = soup.find("lugarnacimiento").string.strip()

                if soup.find("hijos") and soup.find("hijos").string:
                    position.person.metadata["www.senado.es"]["hijos"] = soup.find(
                        "hijos"
                    ).string.strip()

                if soup.find("fallecidofecha") and soup.find("fallecidofecha").string:
                    position.person.metadata["www.senado.es"][
                        "fallecidofecha"
                    ] = soup.find("fallecidofecha").string.strip()

                if soup.find("biografia") and soup.find("biografia").string:
                    position.person.metadata["www.senado.es"]["biografia"] = soup.find(
                        "biografia"
                    ).string.strip()

                if soup.find("legislaturas") and soup.find("legislaturas").string:
                    position.person.metadata["www.senado.es"]["legislaturas"] = []
                    for xml_leg in soup.find_all("legislatura"):
                        leg_data = {
                            "number": int(xml_leg.find("numleg").string.strip()),
                            "start": xml_leg.find("procedfecha").string.strip(),
                        }
                        if (
                            xml_leg.find("bajaliteral")
                            and xml_leg.find("bajaliteral").string
                        ):
                            leg_data["end"] = xml_leg.find("bajaliteral").string.strip()
                        position.person.metadata["www.senado.es"][
                            "legislaturas"
                        ].append(leg_data)

                if (
                    soup.find("legislaturassenado")
                    and soup.find("legislaturassenado").string
                ):
                    position.person.metadata["www.senado.es"]["periods"] = []
                    for xml_leg in soup.find_all("legislaturasenado"):
                        leg_data = {
                            "number": int(
                                xml_leg.find("legantsenlegislatura").string.strip()
                            ),
                            "start": xml_leg.find("legantsenfechaalta").string.strip(),
                        }
                        if (
                            xml_leg.find("legantsenfechabaja")
                            and xml_leg.find("legantsenfechabaja").string
                        ):
                            leg_data["end"] = xml_leg.find(
                                "legantsenfechabaja"
                            ).string.strip()
                        position.person.metadata["www.senado.es"]["periods"].append(
                            leg_data
                        )

                # Save metadata
                position.person.save(update_fields=["metadata"])
                fetched_persons_id.append(position.person.id)

                # Save person birth date
                if position.person.metadata["www.senado.es"].get("fechanacimiento"):
                    date_str = position.person.metadata["www.senado.es"][
                        "fechanacimiento"
                    ]
                    birth_date = (
                        datetime.strptime(date_str, "%d/%m/%Y")
                        .date()
                        .strftime("%Y-%m-%d")
                    )
                    register_birth_date_source(
                        person=position.person,
                        url=url,
                        value=birth_date,
                    )

                # Save person death date
                if position.person.metadata["www.senado.es"].get("fallecidofecha"):
                    date_str = position.person.metadata["www.senado.es"][
                        "fallecidofecha"
                    ]
                    death_date = (
                        datetime.strptime(date_str, "%d/%m/%Y")
                        .date()
                        .strftime("%Y-%m-%d")
                    )
                    register_death_date_source(
                        person=position.person,
                        url=url,
                        value=death_date,
                    )

                # Save person biography
                if position.person.metadata["www.senado.es"].get("biografia"):
                    register_biography_source(
                        person=position.person,
                        url=url,
                        value=position.person.metadata["www.senado.es"]["biografia"],
                    )

                if options["verbosity"] >= 2:
                    logger.info(f"{position.person}")

        if options["verbosity"] >= 2:
            logger.info("Done")
