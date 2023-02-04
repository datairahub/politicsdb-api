# -*- coding: utf-8 -*-
import re
import logging
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.error import HTTPError
from datetime import date
from django.core.management.base import BaseCommand

from people.services.people_id import people_id_from_name
from people.services.names import clean_spanish_name
from core.services.requests import request_page

from people.models import (
    Person,
    BirthSource,
)
from positions.models import (
    Period,
    Position,
)

logger = logging.getLogger("commands")


class Command(BaseCommand):
    """
    Obtener miembros del senado de España desde el índice de
    la página del senado.

    get_senators_from_web() obtiene los siguientes datos:
        - Nombre completo
        - Enlace a la página de detalle del senado
        - Datos raw en metadata['www.senado.es']

    get_senators_data() obtiene información extra de la ficha de cada senador
    para los senadores que proveen dicha ficha. Datos:
        - Sexo
        - Estado civil
        - Lugar de nacimiento
        - Hijos
        - Fecha de nacimiento
        - Fecha de fallecimiento
        - Biografías
        - Legislaturas en el senado
    """

    help = "Update Spain senators"
    search_url = "https://www.senado.es/web/composicionorganizacion/senadores/composicionsenado/senadoresdesde1977/consultaorden/index.html"
    search_data = {
        "legis": "99",  # todas
        "order": "A",
        "boton_obtener_listado": "OBTENER LISTADO",
    }

    def handle(self, *args, **options):
        # self.get_senators_from_web()
        self.get_senators_data()
        logger.info("Done")

    def get_senators_from_web(self):
        for period in Period.objects.filter(
            institution__name="Senado de España"
        ).order_by("-number"):
            logger.info(f"Updating data from senate period {period.number}...")
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
                metadata["group_code"] = sgroup.text
                metadata["group_name"] = sgroup["title"]

                xml = row.select(".col-5")[1].select("a")
                if xml:
                    metadata["xml_data"] = "https://www.senado.es" + xml[0]["href"]

                person, person_created = Person.objects.get_or_create(id_name=id_name)
                if person_created:
                    person.full_name = full_name
                    person.first_name = clean_spanish_name(name_split[1].title())
                    person.last_name = clean_spanish_name(name_split[0].title())
                    person.id_name = people_id_from_name(full_name)
                    person.metadata["www.senado.es"] = {
                        "nombre": name_split[1],
                        "apellidos": name_split[0],
                    }
                    person.metadata["www.senado.es"][
                        f"legislatura-{period.number}"
                    ] = metadata
                else:
                    if not person.metadata.get("www.senado.es", None):
                        person.metadata["www.senado.es"] = {}
                    person.metadata["www.senado.es"]["nombre"] = name_split[1]
                    person.metadata["www.senado.es"]["apellidos"] = name_split[0]
                    person.metadata["www.senado.es"][
                        f"legislatura-{period.number}"
                    ] = metadata

                person.first_name = clean_spanish_name(name_split[1].title())
                person.last_name = clean_spanish_name(name_split[0].title())
                person.save()

                # Senator
                position = Position.objects.filter(person=person, period=period).first()
                if not position:
                    position = Position(person=person, period=period)

                position = Position(
                    period=period,
                    person=person,
                    short_name="Senador",
                    full_name=(f"Senador del {period.institution.name}, {period.name}"),
                    start=date(1900, 1, 1),
                    end=date(1900, 1, 1),
                    metadata={"www.senado.es": metadata},
                )
                position.save()
                logger.info(f"{position} saved")

    def get_senators_data(self, *args, **options):
        fetched_persons_id = []
        # senadoes, created = BirthSource.objects.get_or_create(name='www.senado.es')

        for period in Period.objects.filter(
            institution__name="Senado de España"
        ).order_by("-number"):
            for position in Position.objects.filter(period=period):

                if not position.metadata["www.senado.es"].get("xml_data", None):
                    # senators without open data
                    continue

                if position.metadata["www.senado.es"].get("sexo", None):
                    # senators already fetched (previus executions)
                    continue

                if position.person.id in fetched_persons_id:
                    # senators already fetched (current execution)
                    continue

                url = (
                    position.metadata["www.senado.es"]["xml_data"].split(".xml")[0]
                    + ".xml"
                )
                url = url.replace("web/../", "")
                try:
                    response = request_page(url)
                except HTTPError:
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
                    position.person.metadata["www.senado.es"]["legislaturassenado"] = []
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
                        position.person.metadata["www.senado.es"][
                            "legislaturassenado"
                        ].append(leg_data)

                # Save metadata
                position.person.save(update_fields=["metadata"])
                fetched_persons_id.append(position.person.id)

                # Save person birth date
                if position.person.metadata["www.senado.es"].get(
                    "fechanacimiento", None
                ):
                    birth_date_str = position.person.metadata["www.senado.es"][
                        "fechanacimiento"
                    ]
                    birth_date = datetime.strptime(birth_date_str, "%d/%m/%Y").date()
                    position.person.birth_date = birth_date
                    position.person.save(update_fields=["birth_date"])
                    birth_source = BirthSource.objects.filter(
                        person=position.person,
                        name=urlparse(url).netloc,
                    ).first()
                    if not birth_source:
                        birth_source = BirthSource(
                            person=position.person,
                            name=urlparse(url).netloc,
                        )
                    birth_source.url = url
                    birth_source.is_exact = True

                logger.info(f"{position} saved")
