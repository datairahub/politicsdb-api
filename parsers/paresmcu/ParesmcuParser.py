# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from datetime import datetime


class ParesmcuParser:
    birth_date = None
    birth_date_str = None
    birth_date_is_exact = None
    death_date_str = None
    birth_place = None
    death_place = None
    genre = None
    description = None

    def __init__(self, page):
        self.page = BeautifulSoup(page, "html.parser")
        self.extract_content_data()

    @property
    def is_persona_page(self):
        if not len(self.page.select("h2")):
            return False
        if not self.page.select("#wrapper_ficha .area"):
            return False
        return "Persona" in self.page.select("h2")[0].text

    @property
    def title(self):
        if not len(self.page.select("h2")):
            return None
        return (
            self.page.select("h2")[0]
            .text.replace("\n", "")
            .replace("Persona - ", "")
            .split("(")[0]
            .strip()
        )

    def extract_content_data(self):
        """
        Extract content data
        """
        for p in self.page.select("#wrapper_ficha .area .info"):
            # Iterate over profile page data

            if "fechas de existencia:" in p.text.lower():
                if not len(p.select("span")):
                    continue

                self.birth_date_str = p.select("span")[0].text.strip()
                if len(p.select("span")) == 2:
                    self.death_date_str = p.select("span")[1].text.strip()

                if len(self.birth_date_str) == 4:
                    self.birth_date = datetime.strptime(
                        self.birth_date_str, "%Y"
                    ).date()
                    self.birth_date_is_exact = False

                elif len(self.birth_date_str) == 10:
                    self.birth_date = datetime.strptime(
                        self.birth_date_str, "%Y-%m-%d"
                    ).date()
                    self.birth_date_is_exact = True

                continue

            if "historia:" in p.text.lower():
                if not len(p.select("#historiaNotas > p")):
                    continue
                self.description = " ".join(
                    [t.text for t in p.select("#historiaNotas > p")]
                ).strip()
                continue

            if "lugar de nacimiento:" in p.text.lower():
                if not len(p.select("a")):
                    continue
                if not p.select("a")[0].text.strip():
                    continue
                self.birth_place = p.select("a")[0].text.strip()
                continue

            if "sexo:" in p.text.lower():
                if not len(p.select("a")):
                    continue
                if not p.select("a")[0].text.strip():
                    continue
                self.genre = p.select("a")[0].text.strip()
                continue

            if "lugar de defunci¿n:" in p.text.lower():
                if not len(p.select("a")):
                    continue
                if not p.select("a")[0].text.strip():
                    continue
                self.death_place = p.select("a")[0].text.strip()
                continue
