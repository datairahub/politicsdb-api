# -*- coding: utf-8 -*-
import time
from datetime import datetime, date
import logging
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from organizations.models import Party
from world.models import Adm0

logger = logging.getLogger("commands")


class Command(BaseCommand):
    """ """

    help = "Update Parties"
    sleep = 0.2
    main = "https://servicio.mir.es/nfrontal/webpartido_politico.html"
    search = "https://servicio.mir.es/nfrontal/webpartido_politico/partido_politicoBuscar.html"
    detail_set = "https://servicio.mir.es/nfrontal/webpartido_politico/partido_politicoDatos.html?nmformacion="
    detail = "https://servicio.mir.es/nfrontal/webpartido_politico/recurso/partido_politicoDetalle.html"

    def handle(self, *args, **options):
        adm0 = Adm0.objects.get(code="es")
        session = requests.Session()

        r = session.get(self.main)

        data = {
            "formacionPolitica": "*",
            "siglas": "",
            "tipoFormacion": "",
            "ordenacion": "FECHA",  # or DENOMINACION,
            "fecInsDesdeDia": "",
            "fecInsDesdeMes": "",
            "fecInsDesdeAnyo": "",
            "fecInsHastaDia": "",
            "fecInsHastaMes": "",
            "fecInsHastaAnyo": "",
            "pagActual": 1,
            "tamPag": 10_000,  # 10_000 max
        }
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "es,en;q=0.9,ca;q=0.8",
            "Cache-Control": "max-age=0",
            "Content-Length": "189",
            "Content-Type": "application/x-www-form-urlencoded",
            "DNT": "1",
            "Origin": "https://servicio.mir.es",
            "Referer": "https://servicio.mir.es/nfrontal/webpartido_politico.html",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "Cookie": "; ".join([f"{c[0]}={c[1]}" for c in session.cookies.items()]),
        }
        r = session.post(self.search, data=data, headers=headers)

        soup = BeautifulSoup(r.text, "html.parser")

        parties = []

        for row in soup.select("#resultado tr"):
            name = row.select("a")[0].text
            code = row.select("a")[0]["href"].split("=")[-1]
            address = row.select("td")[1].text
            adm2 = row.select("td")[2].text
            registered = row.select("td")[3].text
            row.find("a").decompose()
            acronim = (
                row.select("td")[0]
                .text.replace("\n", " ")
                .replace(".", "")
                .strip()[1:-1]
            )
            country_code = f"{adm0.code}-{code}"

            party = Party.objects.filter(code=country_code).first()
            if not party:
                party = Party(adm0=adm0, code=country_code, metadata={})
            party.name = name
            party.short_name = acronim
            party.start = datetime.strptime(registered, "%d/%m/%Y").date()
            party.end = date(2999, 12, 31)
            party.address = f"{address} {adm2}".replace("\n", " ").strip()
            while "  " in party.address:
                party.address = party.address.replace("  ", " ")

            if not party.metadata.get("servicio.mir.es"):
                party.metadata["servicio.mir.es"] = {}

            party.metadata["servicio.mir.es"]["name"] = name
            party.metadata["servicio.mir.es"]["acronim"] = acronim
            party.metadata["servicio.mir.es"]["code"] = code
            parties.append(party)

        for party in parties:
            r = session.get(
                f"{self.detail_set}{party.metadata['servicio.mir.es']['code']}"
            )
            r = session.get(self.detail)

            soup = BeautifulSoup(r.text, "html.parser")
            for row in soup.select(".cuerpo .fila"):
                if not row.select("label"):
                    continue
                label = row.select("label")[0]["for"]
                value = row.select("span")[0].text.replace("\t", "").replace("\n", "")
                while "  " in value:
                    value = value.replace("  ", " ")
                value = value.strip()

                if not label in (
                    "simbolo",
                    "promotor",
                    "ambito",
                    "fundacion",
                ):
                    if not value:
                        continue
                    party.metadata["servicio.mir.es"][label] = value.strip()

                elif label == "simbolo":
                    if not row.select("span img"):
                        continue
                    party.metadata["servicio.mir.es"][label] = row.select("span img")[
                        0
                    ]["src"]

                elif label == "promotor":
                    if not party.metadata["servicio.mir.es"].get("promotores"):
                        party.metadata["servicio.mir.es"]["promotores"] = []
                    party.metadata["servicio.mir.es"]["promotores"].append(
                        {
                            "denominacion": row.select("label")[0].text.strip(),
                            "nombre": value,
                        }
                    )

                elif label == "fundacion":
                    if not party.metadata["servicio.mir.es"].get("fundaciones"):
                        party.metadata["servicio.mir.es"]["fundaciones"] = []
                    party.metadata["servicio.mir.es"]["fundaciones"].append(
                        {
                            "nombre": row.select("label")[0].text.strip(),
                            "registro": value,
                        }
                    )

                elif label == "ambito":
                    party.metadata["servicio.mir.es"]["ambito"] = {
                        "tipo": row.select("label")[0].text.strip(),
                        "nombre": value,
                    }

            if not party.metadata["servicio.mir.es"].get("ambito"):
                for title in soup.select(".cuerpo h1"):
                    if title.text.strip() == "Ámbito Territorial":
                        party.metadata["servicio.mir.es"]["ambito"] = {
                            "tipo": str(title.next_sibling),
                        }

            if party.metadata["servicio.mir.es"].get("email"):
                party.email = party.metadata["servicio.mir.es"]["email"]

            if party.metadata["servicio.mir.es"].get("paginaweb"):
                party.web = party.metadata["servicio.mir.es"]["paginaweb"]

            party.save()

            if options["verbosity"] >= 2:
                logger.info(f"{party.name}")

            time.sleep(self.sleep)
