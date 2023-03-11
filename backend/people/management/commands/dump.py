# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from core.services.dump import dump_data


class Command(BaseCommand):
    help = "Dump data"

    def handle(self, *args, **options):
        dump_data()
