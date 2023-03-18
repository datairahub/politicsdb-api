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
    Enrich people's birth date using wikidata project
    "WikiProject every politician". The following data
    are obtained:

    Person:
    - birth_date # Updated always
    - metadata   # Updated always

    https://www.wikidata.org/wiki/Wikidata:WikiProject_every_politician
    """

    help = "Update birth dates using WikiProject_every_politician"
    sleep_time = 1
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
        # "https://www.wikidata.org/wiki/Wikidata:WikiProject_every_politician/Spain/data/Deputies/13th_(bio)"", # Missing
        # "https://www.wikidata.org/wiki/Wikidata:WikiProject_every_politician/Spain/data/Deputies/14th_(bio)"", # Missing
    ]

    def handle(self, *args, **options):
        results = self.get_birth_dates_from_wikidata(*args, **options)

        for result in results.values():
            self.update_birth_date(result, *args, **options)

        if options["verbosity"] >= 2:
            logger.info("Done")

    def update_birth_date(self, result, *args, **options):
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

        if not result["fecha de nacimiento"]:
            return

        register_birth_date_source(
            person=person,
            url=result["wikidata_table_url"],
            value=result["fecha de nacimiento"],
        )

        if options["verbosity"] >= 2:
            logger.info(f"{person}")

    def get_birth_dates_from_wikidata(self, *args, **options):
        results = {}
        for url in self.source_urls:
            if options["verbosity"] >= 2:
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
