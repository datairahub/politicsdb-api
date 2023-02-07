# -*- coding: utf-8 -*-
import re
from datetime import datetime, date
from ..WikiParser import WikiParser


class SpanishWikiParser(WikiParser):
    def is_politician(self) -> bool:
        """
        Check if page is from a politician
        """
        search_politic = re.search(
            r"pol[ií]tic[oa]|senador|diputad[oa]|congreso|alcalde|autoridad", self.text
        )
        return bool(search_politic)

    def get_birth_date(self):
        """
        Get person's birth date
        Returns (date, is_exact:bool) or (None, None)
        """
        # Full date from card
        parsed_date = self.get_full_date_from_authority_card(self.text.lower())
        if parsed_date:
            return parsed_date, True

        text = self.text.lower()
        text = re.sub(
            r"\[\[([^0-9]*?)\]\]?", "", text
        )  # remove links without numbers [[Domingo-Caudillo]]
        text = self.remove_brackets_content(text)
        text = self.remove_html_tags(text)
        text = self.remove_square_brackets(text)
        text = self.remove_double_whitespaces(text)

        # Full date from bio (formatted)
        parsed_date = self.get_full_date_from_bio_with_format(text)
        if parsed_date:
            return parsed_date, True

        # Full date from bio (unformatted)
        parsed_date = self.get_full_date_from_bio_without_format(text)
        if parsed_date:
            return parsed_date, True

        # Partial date from card
        parsed_date = self.get_partial_date_from_authority_card(self.text.lower())
        if parsed_date:
            return parsed_date, False

        # Partial date from bio
        parsed_date = self.get_partial_date_from_bio_with_format(text)
        if parsed_date:
            return parsed_date, False

        # No results
        return None, None

    @staticmethod
    def get_full_date_from_authority_card(text: str):
        """
        Extract full birth date from "ficha autoridad"
        Matchs:
            | fecha de nacimiento = {{fecha|1|1|1962|edad}}
            | fecha de nacimiento = 18 de agosto de [[1944]]
            | fechanac = [[30 noviembre]] de [[1951]]
        """
        text = SpanishWikiParser.remove_double_whitespaces(text)
        structured_dates = re.search(r"fecha de nacimiento =(.+)", text)
        if not structured_dates:
            structured_dates = re.search(r"fechanac =(.+)", text)
        if structured_dates:
            datesrt = structured_dates.group(1).lower().strip()
            datesrt = SpanishWikiParser.clean_authority_card(datesrt)
            datesrt = re.search(r"(\d{1,2}) (\d{1,2}) (\d{4})", datesrt)
            if datesrt:
                return datetime.strptime(
                    f"{datesrt.group(1)} {datesrt.group(2)} {datesrt.group(3)}",
                    "%d %m %Y",
                ).date()
        return None

    @staticmethod
    def get_partial_date_from_authority_card(text: str):
        """
        Extract partial birth date from "ficha autoridad"
        Matchs:
            | fecha de nacimiento = {{fecha|1937}}
            | fecha de nacimiento = {{fecha|5|1937}}
            | fechanac = [[1951]]
            | fechanac = Marzo de [[1951]]
        """
        text = SpanishWikiParser.remove_double_whitespaces(text)
        structured_dates = re.search(r"fecha de nacimiento =(.+)", text)
        if not structured_dates:
            structured_dates = re.search(r"fechanac =(.+)", text)
        if structured_dates:
            datesrt = structured_dates.group(1).lower().strip()
            datesrt = SpanishWikiParser.clean_authority_card(datesrt)
            if datesrt:
                if len(datesrt) == 4:
                    return datetime.strptime(datesrt, "%Y").date()
                if datesrt.count(" ") == 1:
                    return datetime.strptime(datesrt, "%m %Y").date()

    @staticmethod
    def get_full_date_from_bio_with_format(text):
        """
        Extract full birth date (formated) from spanish wikipedia bio.
        Matchs:
            '''alberto''' (irún, guipúzcoa, país vasco (españa), 20 de mayo de 1969)
            '''maría josé lópez santana''' (gines, 12 de enero de 1970-3 de febrero de 2013)
        """
        text = text.replace("(n.", "(")
        bio_date = re.search(
            r"''' \([a-zÀ-ÿø-ÿ0-9 ,;\|\(\)]*?(\d{1,2}) de ([a-zñ]{4,10}) de (\d{4})",
            text,
            re.IGNORECASE,
        )
        if bio_date:
            day = bio_date.group(1)
            month = SpanishWikiParser.named_month_to_number(bio_date.group(2))
            year = bio_date.group(3)
            return date(int(year), int(month), int(day))
        return None

    @staticmethod
    def get_full_date_from_bio_without_format(text):
        """
        Extract full birth date (unformatted) from spanish wikipedia bio.
        Matchs:
            nacido en málaga el 21 de junio de 1955
            nació el 13 de diciembre de 1954 y falleció el 12 de mayo de 1988...
        """
        bio_date = re.search(
            r"(nació|nacid[oa]) [a-zÀ-ÿø-ÿ ,;\|\(\)]+? (\d{1,2}) de ([a-zñ]{4,10}) de (\d{4})",
            text,
            re.IGNORECASE,
        )
        if bio_date:
            day = bio_date.group(2)
            month = SpanishWikiParser.named_month_to_number(bio_date.group(3))
            year = bio_date.group(4)
            return date(int(year), int(month), int(day))
        return None

    @staticmethod
    def get_partial_date_from_bio_with_format(text):
        """
        Extract partial birth date (formatted) from spanish wikipedia bio.
        Matchs:
            '''alberto''' (irún, guipúzcoa, país vasco (españa), 1969)
            '''lorem ''' (laredo (cantabria)|laredo, cantabria; 1950)
        """
        bio_date = re.search(
            r"''' \([a-zÀ-ÿø-ÿ0-9 ,;\.\|\(\)]*?(\d{4})", text, re.IGNORECASE
        )
        if bio_date:
            return date(int(bio_date.group(1)), 1, 1)
        return None

    @staticmethod
    def replace_month_to_num_from_str(date_str):
        """
        Transfrom month to number from a full date string:
        23 de enero de 1998 -> 23 de 1 de 1998
        """
        months = {
            "enero": "1",
            "febrero": "2",
            "marzo": "3",
            "abril": "4",
            "mayo": "5",
            "junio": "6",
            "julio": "7",
            "agosto": "8",
            "septiembre": "9",
            "octubre": "10",
            "noviembre": "11",
            "diciembre": "12",
        }
        for month in months:
            if month in date_str:
                date_str = date_str.lower().replace(month, months.get(month))
        return date_str.strip()

    @staticmethod
    def named_month_to_number(month):
        """
        Convert string month to ordinal
        """
        months = {
            "enero": "01",
            "ene": "01",
            "febrero": "02",
            "feb": "02",
            "marzo": "03",
            "mar": "03",
            "abril": "04",
            "abr": "04",
            "mayo": "05",
            "may": "05",
            "junio": "06",
            "jun": "06",
            "julio": "07",
            "jul": "07",
            "agosto": "08",
            "ago": "08",
            "septiembre": "09",
            "sep": "09",
            "sept": "09",
            "octubre": "10",
            "oct": "10",
            "noviembre": "11",
            "nov": "11",
            "diciembre": "12",
            "dic": "12",
        }
        return months.get(month.lower(), month)

    @staticmethod
    def clean_authority_card(text):
        """
        Remove non-usable characters and strings
        from wikipedia authority card (ficha autoridad)
        """
        text = SpanishWikiParser.remove_brackets(text)
        text = SpanishWikiParser.remove_square_brackets(text)
        text = SpanishWikiParser.remove_html_tags(text)
        text = re.sub(r"fecha de inicio|fecha|edad", "", text)
        text = re.sub(r"\||,|de", " ", text)
        text = SpanishWikiParser.remove_parenthesis_content(text)
        text = SpanishWikiParser.replace_month_to_num_from_str(text)
        text = SpanishWikiParser.remove_non_numbers(text)
        text = SpanishWikiParser.remove_double_whitespaces(text)
        return text
