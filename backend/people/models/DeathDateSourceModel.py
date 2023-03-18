# -*- coding: utf-8 -*-
from core.models import DateSourceAbstractModel


class DeathDateSource(DateSourceAbstractModel):
    """
    Fuente (informativa) para la fecha de fallecimiento
    """

    class Meta(DateSourceAbstractModel.Meta):
        db_table = "people_deathdatesource"
        verbose_name = "Fecha de fallecimiento"
        verbose_name_plural = "Fechas de fallecimiento"
