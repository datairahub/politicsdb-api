# -*- coding: utf-8 -*-
from django.db import models

from persons.services.persons_id import person_id_from_name
from core.models import BaseAbstracModel


class Person(BaseAbstracModel):
    """
    Persona (física)
    """

    GENRES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    full_name = models.CharField(max_length=255, db_index=True)
    id_name = models.CharField(max_length=255, db_index=True, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    genre = models.CharField(choices=GENRES, max_length=1, default=GENRES[0])

    def save(self, *args, **kwargs):
        self.id_name = person_id_from_name(self.full_name)
        super(Person, self).save(*args, **kwargs)

    # def get_person_last_name(self):
    #     if self.metadata.get('www.congreso.es', None):
    #         last_name = None
    #         for legislature_key in self.metadata.get('www.congreso.es'):
    #             last_name = self.metadata['www.congreso.es'][legislature_key].get('apellidos', None)
    #             if last_name:
    #                 return last_name

    #     elif self.metadata.get('www.senado.es'):
    #         return self.metadata['www.senado.es'].get('apellidos', None)

    #     elif self.metadata.get('manual_file'):
    #         return self.metadata['manual_file'].get('last_name', None)

    #     return None

    def __str__(self):
        return self.full_name
