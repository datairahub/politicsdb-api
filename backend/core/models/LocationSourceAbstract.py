# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import GeoHash

from core.models import DataSourceAbstractModel


class LocationSourceAbstractModel(DataSourceAbstractModel):
    value = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        help_text="Nombre de la localización",
    )
    location = models.PointField(
        null=True,
        default=None,
        db_index=True,
        help_text="Coordenadas de la localización",
    )
    location_hash = models.CharField(
        max_length=16,
        db_index=True,
        null=False,
        help_text="Hash de las coordenadas de la localización",
    )

    def save(self, *args, **kwargs):
        self.location_hash = GeoHash(self.location, 8)

    class Meta(DataSourceAbstractModel.Meta):
        abstract = True
