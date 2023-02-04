# -*- coding: utf-8 -*-
from django.db import models
from core.models import BaseAbstracModel


class Institution(BaseAbstracModel):
    """
    Institución (congreso, senado, parlamento autonómico...)
    """

    name = models.CharField(max_length=250, unique=True, db_index=True)
    adm0 = models.ForeignKey("world.Adm0", null=True, on_delete=models.PROTECT)
    adm1 = models.ForeignKey("world.Adm1", null=True, on_delete=models.PROTECT)
    adm2 = models.ForeignKey("world.Adm2", null=True, on_delete=models.PROTECT)
    adm3 = models.ForeignKey("world.Adm3", null=True, on_delete=models.PROTECT)
    adm4 = models.ForeignKey("world.Adm4", null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
