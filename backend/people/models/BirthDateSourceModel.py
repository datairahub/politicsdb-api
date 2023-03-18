# -*- coding: utf-8 -*-
from core.models import DateSourceAbstractModel


class BirthDateSource(DateSourceAbstractModel):
    """
    Fuente (informativa) para la fecha de nacimiento
    """

    class Meta(DateSourceAbstractModel.Meta):
        db_table = "people_birthdatesource"
        verbose_name = "Fecha de nacimiento"
        verbose_name_plural = "Fechas de nacimiento"
