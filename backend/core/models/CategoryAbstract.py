# -*- coding: utf-8 -*-
from django.contrib.gis.db import models

from core.models import BaseModel


class CategoryAbstractModel(BaseModel):
    name = models.CharField(
        max_length=200,
    )
    order = models.IntegerField(
        null=False,
        blank=False,
        default=1,
    )

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        abstract = True
