# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from datetime import date


class FPabloIglesiasParser:
    position = None
    birth_date = None
    birth_date_str = None
    birth_date_is_exact = None
    description = None
    is_parsed = False

    def __init__(self, page):
        self.page = BeautifulSoup(page, "html.parser")
        if len(self.page.select(".entry-content")) == 1:
            self.content = self.page.select(".entry-content")[0]
            self.extract_content_data()
            self.is_parsed = True

    @property
    def title(self):
        """
        Get page title
        """
        title = self.page.find("title")
        if not title:
            return None
        return title.text.replace(" - Fundación Pablo Iglesias", "")

    @property
    def images(self):
        """
        Get content images
        """
        return [img["src"] for img in self.content.select("img")]

    def extract_content_data(self):
        """
        Extract content data
        """
        for p in self.content.select("p"):
            if "cargo:" in p.text.lower():
                self.position = p.text.replace("Cargo:", "").strip()
                continue

            if "nacimiento:" in p.text.lower():
                birth = p.text.replace("Nacimiento:", "").strip()
                if not birth:
                    continue

                # Search full date
                birth_date_search = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", birth)
                if birth_date_search:
                    self.birth_date = date(
                        int(birth_date_search.group(3)),
                        int(birth_date_search.group(2)),
                        int(birth_date_search.group(1)),
                    )
                    self.birth_date_is_exact = True
                    self.birth_date_str = birth_date_search.group(0)
                    continue

                # Search partial date
                birth_date_search = re.search(r"\d{4}", birth)
                if birth_date_search:
                    self.birth_date = date(int(birth_date_search.group(0)), 1, 1)
                    self.birth_date_is_exact = False
                    self.birth_date_str = birth_date_search.group(0)
                continue

            if "biografía:" in p.text.lower():
                self.description = (
                    p.text.replace("Biografía:", "").replace("\n", " ").strip()
                )
