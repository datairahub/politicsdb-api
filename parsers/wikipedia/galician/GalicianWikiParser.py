# -*- coding: utf-8 -*-
import re
from datetime import datetime, date
from ..WikiParser import WikiParser


class GalicianWikiParser(WikiParser):
    def is_politician(self) -> bool:
        """
        Check if page is from a politician
        """
        search_politic = re.search(
            r"pol[ií]tic[oa]|senador|deputad[oa]|congreso|alcalde|autoridad", self.text
        )
        return bool(search_politic)

    def get_birth_date(self) -> str:
        """
        Get person's birth date
        """
        # Full date from card
        parsed_date = self.get_full_date_from_authority_card(self.text.lower())
        if parsed_date:
            return parsed_date

        text = self.remove_brackets_content(self.text.lower())
        text = self.remove_html_tags(text)
        text = self.remove_square_brackets(text)
        text = self.remove_parenthesis(text)
        text = self.remove_double_whitespaces(text)

        # Full date from bio
        parsed_date = self.get_full_date_from_bio_without_format(text)
        if parsed_date:
            return parsed_date

        # Partial date from bio
        parsed_date = self.get_partial_date_from_bio_without_format(text)
        if parsed_date:
            return parsed_date

        return None

    @staticmethod
    def get_full_date_from_authority_card(text: str) -> str:
        """
        Extract full birth date from "ficha autoridad"
        Matchs:
            | datanac = [[27 de marzo]] de [[1955]]
            | datanac    = {{data|25|2|1953|idade}}
            |data de nacemento = [[5 de xaneiro]] de [[1938]] {{Idade|5|1|1938}}
            datadenacemento = [[7 de xuño]] de [[1948]]|
        """
        structured_dates = re.search(r"data de nacemento =(.+)", text)

        if not structured_dates:
            structured_dates = re.search(r"datadenacemento =(.+)", text)

        if not structured_dates:
            structured_dates = re.search(r"datanac =(.+)", text)

        if structured_dates:
            datesrt = structured_dates.group(1).lower().strip()
            datesrt = GalicianWikiParser.clean_authority_card(datesrt)
            datesrt = re.search(r"(\d{1,2}) (\d{1,2}) (\d{4})", datesrt)
            if datesrt:
                return (
                    datetime.strptime(
                        f"{datesrt.group(1)} {datesrt.group(2)} {datesrt.group(3)}",
                        "%d %m %Y",
                    )
                    .date()
                    .strftime("%Y-%m-%d")
                )

        return None

    @staticmethod
    def get_full_date_from_bio_without_format(text):
        """
        Extract full birth date (unformatted) from galician wikipedia bio.
        Matchs:
            nado en Málaga o 21 de xunio de 1955
            nado o 25 de febreiro de 1953 en Madrid
            nado en Pozuelo, Madrid o 14 de abril de 1926 e finado o 3 de maio de 2008
            nada en Cebreros (provincia de Ávila) o 25 de setembro de 1932
        """
        bio_date = re.search(
            r" nad[ao] [a-zÀ-ÿø-ÿ ,\|0-9\(\)]+? (\d{1,2}) de ([a-zñ]{4,9}) de (\d{4})",
            text,
            re.IGNORECASE,
        )
        if bio_date and not (
            "finad" in bio_date.group(0) or "falecid" in bio_date.group(0)
        ):
            day = bio_date.group(1)
            month = GalicianWikiParser.named_month_to_number(bio_date.group(2))
            year = bio_date.group(3)
            return date(int(year), int(month), int(day)).strftime("%Y-%m-%d")

        return None

    @staticmethod
    def get_partial_date_from_bio_without_format(text):
        """
        Extract partial birth date (unformatted) from galician wikipedia bio.
        Matchs:
            nado en Málaga en 1955
            nada en Nador (Marrocos) en 1952
        """
        bio_date = re.search(
            r" nad[ao] [a-zÀ-ÿø-ÿ ,\|0-9\(\)]+? (\d{4})", text, re.IGNORECASE
        )
        if bio_date and not (
            "finad" in bio_date.group(0) or "falecid" in bio_date.group(0)
        ):
            return bio_date.group(1)

        return None

    @staticmethod
    def replace_month_to_num_from_str(date_str):
        """
        Transfrom month to number from a full date string:
        23 de xaneiro de 1998 -> 23 de 1 de 1998
        """
        months = {
            "xaneiro": "1",
            "febreiro": "2",
            "marzo": "3",
            "marzal": "3",
            "abril": "4",
            "maio": "5",
            "xunio": "6",
            "xuño": "6",
            "xullo": "7",
            "xulio": "7",
            "agosto": "8",
            "setembro": "9",
            "outubro": "10",
            "novembro": "11",
            "decembro": "12",
            "nadal": "12",
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
            "xaneiro": "01",
            "xan": "01",
            "febreiro": "02",
            "feb": "02",
            "marzal": "03",
            "marzo": "03",
            "mar": "03",
            "abril": "04",
            "abr": "04",
            "maio": "05",
            "mai": "05",
            "xunio": "06",
            "xuño": "06",
            "xuñ": "06",
            "xullo": "07",
            "xul": "07",
            "agosto": "08",
            "ago": "08",
            "setembro": "09",
            "sep": "09",
            "set": "09",
            "outubro": "10",
            "oct": "10",
            "out": "10",
            "novembro": "11",
            "nov": "11",
            "decembro": "12",
            "dec": "12",
            "nadal": "12",
            "nad": "12",
        }
        return months.get(month.lower(), month.lower())

    @staticmethod
    def clean_authority_card(text):
        """
        Remove non-usable characters and strings
        from wikipedia authority card (ficha autoridad)
        """
        text = GalicianWikiParser.remove_brackets(text)
        text = GalicianWikiParser.remove_square_brackets(text)
        text = GalicianWikiParser.remove_html_tags(text)
        text = text.replace("data", "").replace("idade", "").strip()
        text = text.replace("|", " ").replace(",", " ").strip()
        text = text.replace("de", " ").strip()
        text = GalicianWikiParser.remove_parenthesis_content(text)
        text = GalicianWikiParser.replace_month_to_num_from_str(text)
        text = GalicianWikiParser.remove_non_numbers(text)
        text = GalicianWikiParser.remove_double_whitespaces(text)
        return text
