# -*- coding: utf-8 -*-
from core.models import LocationSourceAbstractModel


class BirthPlaceSource(LocationSourceAbstractModel):
    """
    Fuente (informativa) para el lugar de nacimiento
    """

    class Meta(LocationSourceAbstractModel.Meta):
        db_table = "people_birthplacesource"
        verbose_name = "Lugar de nacimiento"
        verbose_name_plural = "Lugares de nacimiento"
