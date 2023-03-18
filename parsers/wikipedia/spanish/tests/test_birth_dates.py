# -*- coding: utf-8 -*-
import sys
import unittest
from datetime import date
from django.conf import settings

sys.path.append(str(settings.BASE_DIR.parent))
from parsers.wikipedia import SpanishWikiParser


class SpanishWikiParserBirthDatesTests(unittest.TestCase):
    """
    Tests for class SpanishWikiParser related to birth date extraction
    """

    def test_birth_date_extraction(self):
        """
        Correnct birth dates are extracted from wikipedia raw content
        """

        class Page(object):
            pass

        page = Page()
        strings_and_dates = [
            [
                "'''León Rodríguez''' ([[Santo Domingo-Caudilla|Santo Domingo]], [[11 de abril]] de [[1909]] - [[Madrid]], [[9 de septiembre]] de [[1997]])",
                "1909-04-11",
            ],
            [
                "'''Francisco Javier Máximo Aguirre de la Hoz''' ([[Ávila]], [[1946]]-[[2013]]) fue un abogado y [[político]] [[España|español]].",
                "1946",
            ],
            [
                "'''Jesús Aizpún Tuero''' ([[Pamplona]], [[17 de junio]] de [[1928]] - ''[[Ibidem]]''., [[29 de diciembre]] de [[1999]])",
                "1928-06-17",
            ],
            [
                "'''Manuel Benítez Rufo''' ([[Monterrubio de la Serena]], [[Provincia de Badajoz|Badajoz]], [[16 de noviembre]] de [[1917]] – [[Dos Hermanas]], [[Provincia de Sevilla|Sevilla]], [[29 de julio]] de [[2004]])",
                "1917-11-16",
            ],
            [
                "'''Manuel Bermejo Hernández''' ([[Plasencia (Cáceres)|Plasencia]], [[provincia de Cáceres]], [[26 de marzo]] de [[1936]] - [[Madrid]], [[22 de septiembre]] de [[2009]])",
                "1936-03-26",
            ],
            [
                "'''Ramón Germinal Bernal Soto''' (n.{{esd}}[[Linares (Jaén)|Linares]], 22 de mayo de 1924)",
                "1924-05-22",
            ],
            [
                "'''Esteban Caamaño Bernal''', [[sindicalista]] y [[político]] nacido en [[El Puerto]], provincia de [[Cádiz]], el 25 de diciembre de 1925 y fallecido el 19 de junio de 2006.",
                "1925-12-25",
            ],
            [
                "'''Jesús Hervella García''' ([[1926]] - [[Palencia]], [[29 de abril]] de [[2009]])",
                "1926",
            ],
            [
                "'''José Ramón Lasuén Sancho'''<ref>{{Cita web|url=http://www.ediciones2010.es/losautores/jose_ramon_lasuen_sancho.html|título=Ediciones 2010 - José Ramón Lasuen Sancho|fechaacceso=15 de marzo de 2016|apellido=MAGS|sitioweb=www.ediciones2010.es}}</ref> ([[Alcañiz]], [[provincia de Teruel]], [[20 de noviembre]] de [[1932]])",
                "1932-11-20",
            ],
            [
                "'''Miguel Ángel Vázquez Bermúdez''' ([[Sevilla]], 1965) es un político español. Ha sido [[Junta de Andalucía|portavoz del Gobierno de la Junta de Andalucía]] desde el 8 de mayo de 2012 hasta el 9 de junio de 2017",
                "1965",
            ],
            ["| fecha de nacimiento = [[1935]]", "1935"],
            [
                "| fecha de nacimiento = 14 de noviembre de 1914",
                "1914-11-14",
            ],
            ["| fechanac = [[21 de julio]] de [[1928]]", "1928-07-21"],
            [
                "| fecha de nacimiento    = [[28 de abril]] de [[1935]] ({{edad|28|4|1935}})",
                "1935-04-28",
            ],
            [
                "| fecha de nacimiento = [[1939]] '''Carlota Bustelo García del Real''' ([[Madrid]], [[1 de noviembre]] de [[1939]]",
                "1939-11-01",
            ],
        ]
        for str_and_date in strings_and_dates:
            page.text = str_and_date[0]
            parser = SpanishWikiParser(page)
            extracted_date = parser.get_birth_date()
            self.assertEqual(
                str_and_date[1],
                extracted_date,
                f'Date parser failed for "{str_and_date[0]}"',
            )

    def test_formatted_birth_dates_are_extracted_from_bio(self):
        """
        Correct birth dates are extracted from wikipedia pages
        when date is correctly formatted (wikipedia conventions)
        """
        strings_and_dates = [
            [
                "'''lorem''' (irún, guipúzcoa, país vasco (españa), 20 de mayo de 1969)",
                "1969-05-20",
            ],
            [
                "'''lorem ''' (laredo (cantabria)|laredo, cantabria; 14 de octubre de 1950)",
                "1950-10-14",
            ],
            [
                "'''lorem''' (torres (jaén)|torres, provincia de jaén (españa)|jaén, 26 de octubre de 1955)",
                "1955-10-26",
            ],
            [
                "'''lorem''' (n. cádiz, españa; 15 de diciembre de 1947)",
                "1947-12-15",
            ],
            [
                "'''lorem''' (motilla del palancar, cuenca (españa)|cuenca, españa, 25 de noviembre de 1989)",
                "1989-11-25",
            ],
            ["'''lorem''' (bilbao, 27 de diciembre de 1976)", "1976-12-27"],
            [
                "'''lorem''' (n. las palmas de gran canaria, 28 de septiembre de 1958)",
                "1958-09-28",
            ],
            [
                "'''lorem''', más conocida como '''ipsum''' (melilla, 22 de septiembre de 1953)",
                "1953-09-22",
            ],
            [
                "'''lorem''' (puebla de sanabria, provincia de zamora|zamora, 30 de julio de 1956)",
                "1956-07-30",
            ],
            [
                "'''lorem''' (gines, 12 de enero de 1970 - 3 de febrero de 2013)",
                "1970-01-12",
            ],
            ["'''lorem''' (13 de noviembre de 1954)", "1954-11-13"],
            [
                "'''lorem''' (domingo, 11 de abril de 1909 - madrid, 9 de enero de 1997)",
                "1909-04-11",
            ],
        ]
        for str_and_date in strings_and_dates:
            extracted_date = SpanishWikiParser.get_full_date_from_bio_with_format(
                str_and_date[0]
            )
            self.assertEqual(
                str_and_date[1],
                extracted_date,
                f'Parser failed for "{str_and_date[0]}"',
            )

    def test_unformatted_birth_dates_are_extracted_from_bio(self):
        """
        Correct birth dates are extracted from wikipedia pages
        when date is placed in the bio without wikipedia's convention format
        """
        strings_and_dates = [
            ["nacido en málaga el 21 de junio de 1955", "1955-06-21"],
            [
                "nació el 13 de diciembre de 1954 y falleció el 12 de mayo de 1988...",
                "1954-12-13",
            ],
            [
                "nacido en san cristóbal de la laguna (tenerife, canarias) el 12 de mayo de 1954. El 13 de mayo de 1982...",
                "1954-05-12",
            ],
            ["Nacida en ponferrada (león) el 9 de mayo de 1957", "1957-05-09"],
        ]
        for str_and_date in strings_and_dates:
            extracted_date = SpanishWikiParser.get_full_date_from_bio_without_format(
                str_and_date[0]
            )
            self.assertEqual(
                str_and_date[1],
                extracted_date,
                f'Parser failed for "{str_and_date[0]}"',
            )

    def test_wrong_unformatted_birth_dates_are_not_extracted_from_bio(self):
        """
        Incorrect dates are not extracted from wikipedia pages
        when date is placed in the bio without wikipedia's convention format
        """
        strings = [
            "nacido en málaga. El 21 de junio de 1955 escribió",
            "nació en 1954 en Lugo y falleció el 12 de mayo de 1988",
        ]
        for string in strings:
            extracted_date = SpanishWikiParser.get_full_date_from_bio_without_format(
                string
            )
            self.assertIsNone(
                extracted_date, f'Parser extracted wrong date for "{string}"'
            )

    def test_formatted_partial_birth_dates_are_extracted_from_bio(self):
        """
        Correct birth dates are extracted from wikipedia pages
        when partial date is correctly formatted (wikipedia conventions)
        """
        strings_and_dates = [
            ["'''lorem''' (lugar de alicante, 1958)", "1958"],
            [
                "'''lorem''' (irún, guipúzcoa, país vasco (españa), 1969)",
                "1969",
            ],
            [
                "'''lorem''' (laredo (cantabria)|laredo, cantabria; 1950)",
                "1950",
            ],
            [
                "'''lorem''' (torres (jaén)|torres, provincia de jaén (españa)|jaén, 1955)",
                "1955",
            ],
            ["'''lorem''' (n. cádiz, españa; 1947)", "1947"],
            [
                "'''lorem''' (motilla del palancar, cuenca (españa)|cuenca, españa, 1989) (este 1234)",
                "1989",
            ],
            ["'''lorem''' (bilbao, 1976) lorem 2012", "1976"],
            ["'''lorem''' (n. las palmas de gran canaria, 1958)", "1958"],
            [
                "'''lorem''', más conocida como '''ipsum''' (melilla, 1953)",
                "1953",
            ],
            [
                "'''lorem''' (puebla de sanabria, provincia de zamora|zamora, 1956)",
                "1956",
            ],
            ["'''lorem''' (gines, 1970-3 de febrero de 2013)", "1970"],
            [
                "'''lorem''' (españa, 1949 - zaragoza, 27 de enero de 2022)",
                "1949",
            ],
            [
                "'''lorem''' (n. en tollo, vega de liébana, cantabria, en 1945)",
                "1945",
            ],
            ["'''lorem''' (1926 - palencia, 29 de abril de 2009)", "1926"],
        ]
        for str_and_date in strings_and_dates:
            extracted_date = SpanishWikiParser.get_partial_date_from_bio_with_format(
                str_and_date[0]
            )
            self.assertEqual(
                str_and_date[1],
                extracted_date,
                f'Parser failed for "{str_and_date[0]}"',
            )

    def test_wrong_formatted_partial_birth_dates_are_not_extracted_from_bio(self):
        """
        Incorrect birth dates are not extracted from wikipedia pages
        when partial date is correctly formatted (wikipedia conventions)
        """
        strings = [
            "'''lorem''' (sevilla - zaragoza, 27 de enero de 2022)",
            "'''lorem''' (n. sevilla - zaragoza, 27 de enero de 2022)",
            "'''lorem''' (bilbao-1976) lorem 2012",
        ]
        for string in strings:
            extracted_date = SpanishWikiParser.get_partial_date_from_bio_with_format(
                string
            )
            self.assertIsNone(
                extracted_date, f'Parser extracted wrong date for "{string}"'
            )

    def test_full_birth_dates_are_extracted_from_card(self):
        """
        Correct full birth dates are extracted from wikipedia pages
        with authority card
        """
        strings_and_dates = [
            ["| fecha de nacimiento = {{fecha|12|1|1962|edad}}", "1962-01-12"],
            ["| fecha de nacimiento = 18 de agosto de [[1944]]", "1944-08-18"],
            ["| fecha de nacimiento = 30 noviembre [[1922]]", "1922-11-30"],
            ["| fechanac = [[30 de noviembre]] de [[1951]]", "1951-11-30"],
            [
                "| fecha de nacimiento = [[28 de abril]] de [[1935]] ({{edad|28|4|1935}})",
                "1935-04-28",
            ],
        ]
        for str_and_date in strings_and_dates:
            extracted_date = SpanishWikiParser.get_full_date_from_authority_card(
                str_and_date[0]
            )
            self.assertEqual(
                str_and_date[1],
                extracted_date,
                f'Parser failed for "{str_and_date[0]}"',
            )

    def test_partial_birth_dates_are_extracted_from_card(self):
        """
        Correct partial birth dates are extracted from wikipedia pages
        with authority card
        """
        strings_and_dates = [
            ["| fecha de nacimiento = {{fecha|1937}}", "1937"],
            ["| fecha de nacimiento = {{fecha|5|1937}}", "1937-05"],
            ["| fechanac = [[1951]]", "1951"],
            ["| fechanac = Marzo de [[1951]]", "1951-03"],
        ]
        for str_and_date in strings_and_dates:
            extracted_date = SpanishWikiParser.get_partial_date_from_authority_card(
                str_and_date[0]
            )
            self.assertEqual(
                str_and_date[1],
                extracted_date,
                f'Parser failed for "{str_and_date[0]}"',
            )
