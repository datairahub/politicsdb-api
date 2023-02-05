# -*- coding: utf-8 -*-
import time
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
    Obtener fechas de nacimiento de wikidata usando el proyecto
    "WikiProject every politician"
    https://www.wikidata.org/wiki/Wikidata:WikiProject_every_politician
    """

    help = "Update birth dates using WikiProject_every_politician"
    sleep_time = 0
    source_urls = [
        "https://www.wikidata.org/wiki/Wikidata:WikiProject_every_politician/Spain/data/Deputies/constituent_(bio)",
        "https://www.wikidata.org/wiki/Wikidata:WikiProject_every_politician/Spain/data/Deputies/1st_(bio)",
        "https://www.wikidata.org/wiki/Wikidata:WikiProject_every_politician/Spain/data/Deputies/2nd_(bio)",
        "https://www.wikidata.org/wiki/Wikidata:WikiProject_every_politician/Spain/data/Deputies/3rd_(bio)",
        "https://www.wikidata.org/wiki/Wikidata:WikiProject_every_politician/Spain/data/Deputies/4th_(bio)",
        "https://www.wikidata.org/wiki/Wikidata:WikiProject_every_politician/Spain/data/Deputies/5th_(bio)",
        "https://www.wikidata.org/wiki/Wikidata:WikiProject_every_politician/Spain/data/Deputies/6th_(bio)",
        "https://www.wikidata.org/wiki/Wikidata:WikiProject_every_politician/Spain/data/Deputies/7th_(bio)",
        "https://www.wikidata.org/wiki/Wikidata:WikiProject_every_politician/Spain/data/Deputies/8th_(bio)",
        "https://www.wikidata.org/wiki/Wikidata:WikiProject_every_politician/Spain/data/Deputies/9th_(bio)",
        "https://www.wikidata.org/wiki/Wikidata:WikiProject_every_politician/Spain/data/Deputies/10th_(bio)",
        "https://www.wikidata.org/wiki/Wikidata:WikiProject_every_politician/Spain/data/Deputies/11th_(bio)",
        "https://www.wikidata.org/wiki/Wikidata:WikiProject_every_politician/Spain/data/Deputies/12th_(bio)",
        # 'https://www.wikidata.org/wiki/Wikidata:WikiProject_every_politician/Spain/data/Deputies/13th_(bio)', # Missing
        # 'https://www.wikidata.org/wiki/Wikidata:WikiProject_every_politician/Spain/data/Deputies/14th_(bio)', # Missing
    ]

    def handle(self, *args, **options):
        results = self.get_birth_dates_from_wikidata()
        for result in results.values():
            self.update_birth_date(result)
        logger.info("Done")

    def update_birth_date(self, result):
        if not result.get("fecha de nacimiento"):
            # birth date not found
            return

        person = Person.objects.filter(id_name=result["id_name"]).first()

        if not person:
            person = Person.objects.filter(
                id_name__startswith=result["id_name"]
            ).first()
            if not person:
                return

        if not person.metadata.get("www.wikidata.org"):
            person.metadata["www.wikidata.org"] = {}

        person.metadata["www.wikidata.org"]["wikiproject_every_politician"] = result
        person.save(update_fields=["metadata"])

        birth_date, is_exact = self.get_birth_date_from_result(
            result["fecha de nacimiento"]
        )

        if not birth_date:
            return

        register_birth_date_source(
            person, result["wikidata_table_url"], birth_date, is_exact
        )

        if not person.birth_date:
            # update person birth date if it's empty
            person.birth_date = birth_date
            person.save(update_fields=["birth_date"])
            logger.info(f"{person} birth date updated")

        elif person.birth_date != birth_date and is_exact:
            # if previous date is set and its not the same, skip
            logger.warn(
                f"Different dates for {person}: {person.birth_date} -> {birth_date}"
            )

    def get_birth_dates_from_wikidata(self):
        results = {}
        for url in self.source_urls:
            logger.info(f"Collectiong data from {url}")
            response = request_page(url)
            time.sleep(self.sleep_time)
            soup = BeautifulSoup(response, "html.parser")
            table = soup.select(".wikitable")[0]
            headers = [
                col.text.replace("\n", "").lower().strip()
                for col in table.select("tr th")
            ]
            for rowidx, row in enumerate(table.select("tbody tr")):
                if rowidx == 0:
                    continue
                result = {}
                if row.get("class", None):
                    result["wikidata_id"] = row["class"][0].replace("wd_", "").upper()
                for colidx, col in enumerate(row.select("td")):
                    result[headers[colidx]] = str(col.text.replace("\n", "")).strip()
                result["clean_name"] = clean_spanish_name(result["name"])
                result["id_name"] = people_id_from_name(result["clean_name"])
                result["wikidata_table_url"] = url

                if results.get(result["id_name"], None):
                    # check if data is incomplete
                    stored = results.get(result["id_name"])
                    for key in result:
                        if not stored.get(key):
                            results[result["id_name"]][key] = result[key]
                else:
                    results[result["id_name"]] = result

        return results

    def get_birth_date_from_result(self, strdate: str) -> tuple:
        if len(strdate) == 4:
            return datetime.strptime(strdate, "%Y").date(), False
        if len(strdate) == 7:
            return datetime.strptime(strdate, "%Y-%m").date(), False
        if len(strdate) == 10:
            return datetime.strptime(strdate, "%Y-%m-%d").date(), True
        return None, None
