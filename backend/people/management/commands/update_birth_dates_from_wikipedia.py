# -*- coding: utf-8 -*-
import sys
import logging
import pywikibot
from django.conf import settings

sys.path.append(str(settings.BASE_DIR.parent))
from wikipedia import SpanishWikiParser, GalicianWikiParser
from django.core.management.base import BaseCommand
from people.models import Person, BirthSource

logger = logging.getLogger("commands")


class Command(BaseCommand):
    help = "Update birth dates using wikipedia"

    def handle(self, *args, **options):
        self.update_birth_dates_from_wikipedia()
        logger.info("Done")

    def update_birth_dates_from_wikipedia(self):
        for person in Person.objects.filter(birth_date=None):
            # Update birth dates using es.wikipedia.org
            birth_date, is_exact, url = self.get_birth_date_from_spanish_wikipedia(
                person
            )

            if not birth_date:
                # Update birth dates using gl.wikipedia.org
                birth_date, is_exact, url = self.get_birth_date_from_galician_wikipedia(
                    person
                )

            if not birth_date:
                continue

            person.birth_date = birth_date
            person.save(update_fields=["birth_date"])

            if not BirthSource.objects.filter(person=person, url=url).exists():
                # birth source not registered yet
                BirthSource(
                    person=person,
                    url=url,
                    is_exact=is_exact,
                    date=birth_date,
                ).save()

            logger.info(f"{person} birth date updated")

    def get_birth_date_from_spanish_wikipedia(self, person):
        site = pywikibot.Site("es", "wikipedia")
        page = pywikibot.Page(site, person.full_name)

        while page.isRedirectPage():
            page = page.getRedirectTarget()

        if not (page and page.text.strip()):
            return None, None, None

        parser = SpanishWikiParser(page)
        if not parser.is_politician():
            return None, None, None

        date, exact = parser.get_birth_date()
        return date, exact, page.full_url()

    def get_birth_date_from_galician_wikipedia(self, person):
        site = pywikibot.Site("gl", "wikipedia")
        page = pywikibot.Page(site, person.full_name)

        while page.isRedirectPage():
            page = page.getRedirectTarget()

        if not (page and page.text.strip()):
            return None, None, None

        parser = GalicianWikiParser(page)
        if not parser.is_politician():
            return None, None, None

        date, exact = parser.get_birth_date()
        return date, exact, page.full_url()
