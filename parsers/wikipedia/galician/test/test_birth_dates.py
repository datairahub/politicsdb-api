# -*- coding: utf-8 -*-
import sys
import unittest
from datetime import date
from django.conf import settings

sys.path.append(str(settings.BASE_DIR.parent))
from parsers.wikipedia import GalicianWikiParser


class GalicianWikiParserBirthDatesTests(unittest.TestCase):
    """
    Tests for class GalicianWikiParser related to birth date extraction
    """

    def test_full_birth_dates_are_extracted_from_bio(self):
        """
        Correct birth dates are extracted from pages
        when date is placed in the bio
        """
        strings_and_dates = [
            [" nado o 25 de febreiro de 1953 en Madrid", "1953-02-25"],
            [" nado en Málaga o 21 de xunio de 1955", "1955-06-21"],
            [
                " nada en Cebreros (provincia de Ávila) o 25 de setembro de 1932",
                "1932-09-25",
            ],
            [
                " nado en Pozuelo, Madrid o 14 de abril de 1926 e finado o 3 de maio de 2008",
                "1926-04-14",
            ],
        ]
        for str_and_date in strings_and_dates:
            extracted_date = GalicianWikiParser.get_full_date_from_bio_without_format(
                str_and_date[0]
            )
            self.assertEqual(
                str_and_date[1],
                extracted_date,
                f'Parser failed for "{str_and_date[0]}"',
            )

    def test_wrong_full_birth_dates_are_not_extracted_from_bio(self):
        """
        Incorrect dates are not extracted from wikipedia pages
        when date is placed in the bio
        """
        strings = [
            " nada en Ávila e finada o 25 de setembro de 1932",
            " nado en Madrid en 1908 e falecido na mesma cidade o 27 de novembro de 1989",
            "Andrés de Losada e Prada, finado en Madrid o 8 de decembro de 1625",
            "é unha investigadora que desde o 20 de xullo de 2018 exerce",
        ]
        for string in strings:
            extracted_date = GalicianWikiParser.get_full_date_from_bio_without_format(
                string
            )
            self.assertIsNone(
                extracted_date, f'Parser extracted wrong date for "{string}"'
            )

    def test_partial_birth_dates_are_extracted_from_bio(self):
        """
        Correct birth dates are extracted from wikipedia pages
        when partial date is in bio
        """
        strings_and_dates = [
            [" nado en Málaga en 1955", "1955"],
            [" nada en Nador (Marrocos) en 1952", "1952"],
            [" nada en 1945", "1945"],
        ]
        for str_and_date in strings_and_dates:
            extracted_date = (
                GalicianWikiParser.get_partial_date_from_bio_without_format(
                    str_and_date[0]
                )
            )
            self.assertEqual(
                str_and_date[1],
                extracted_date,
                f'Parser failed for "{str_and_date[0]}"',
            )

    def test_full_birth_dates_are_extracted_from_card(self):
        """
        Correct full birth dates are extracted from wikipedia pages
        with authority card
        """
        strings_and_dates = [
            ["| datanac = [[27 de marzo]] de [[1955]]", "1955-03-27"],
            ["| datanac = {{data|25|2|1953|idade}}", "1953-02-25"],
            [
                "| data de nacemento = [[5 de xaneiro]] de [[1938]] {{Idade|5|1|1938}}",
                "1938-01-05",
            ],
            ["| datadenacemento = [[7 de xuño]] de [[1948]]|", "1948-06-07"],
        ]
        for str_and_date in strings_and_dates:
            extracted_date = GalicianWikiParser.get_full_date_from_authority_card(
                str_and_date[0]
            )
            self.assertEqual(
                str_and_date[1],
                extracted_date,
                f'Parser failed for "{str_and_date[0]}"',
            )
