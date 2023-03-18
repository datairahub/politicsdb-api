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

from people.services.people_id import people_id_from_name
from people.services.names import clean_spanish_name
from people.services.birth_dates import register_birth_date_source
from people.services.death_dates import register_death_date_source
from people.services.biographies import register_biography_source
from core.services.requests import request_page

from people.models import (
    Person,
)
from positions.models import (
    Period,
    Position,
)

logger = logging.getLogger("commands")


class Command(BaseCommand):
    """
    Obtener miembros del senado de España desde la página del senado.

    get_senators_from_index() obtiene los siguientes datos:
        - Nombre completo
        - Enlace a la página de detalle del senado
        - Datos raw en metadata['www.senado.es']

    get_senators_open_data() obtiene información de la ficha de datos abiertos
    de cada senador. Datos:
        - Sexo
        - Estado civil
        - Lugar de nacimiento
        - Hijos
        - Fecha de nacimiento
        - Fecha de fallecimiento
        - Biografías
        - Legislaturas en el senado

    get_senators_page_data() obtiene información de la página de detalle de cada
    senador. Datos:
        - Fecha de alta
        - Fecha de baja
        - Imagen
    """

    help = "Update Spain senators"
    search_url = "https://www.senado.es/web/composicionorganizacion/senadores/composicionsenado/senadoresdesde1977/consultaorden/index.html"
    search_data = {
        "legis": "99",  # todas
        "order": "A",
        "boton_obtener_listado": "OBTENER LISTADO",
    }
    sleep_time = 0.5

    def handle(self, *args, **options):
        self.get_senators_from_index(*args, **options)
        self.get_senators_open_data(*args, **options)
        self.get_senators_page_data(*args, **options)
        if options["verbosity"] >= 2:
            logger.info("Done")

    def get_senators_from_index(self, *args, **options):
        for period in Period.objects.filter(
            institution__name="Senado de España"
        ).order_by("-number"):
            if options["verbosity"] >= 2:
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
                person.metadata["www.senado.es"]["nombre"] = name_split[1]
                person.metadata["www.senado.es"]["apellidos"] = name_split[0]
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
                    logger.info(f"{position} saved")

    def get_senators_open_data(self, *args, **options):
        fetched_persons_id = []

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
                    logger.info(f"{position} saved")

    def get_senators_page_data(self, *args, **options):
        last_period = (
            Period.objects.filter(institution__name="Senado de España")
            .order_by("number")
            .last()
        )

        for position in Position.objects.filter(
            period__institution__name="Senado de España"
        ):
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
                # current period
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
                logger.info(f"{position} saved")

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
