# -*- coding: utf-8 -*-
from core.models import LocationSourceAbstractModel


class DeathPlaceSource(LocationSourceAbstractModel):
    """
    Fuente (informativa) para el lugar de fallecimiento
    """

    class Meta(LocationSourceAbstractModel.Meta):
        db_table = "people_deathplacesource"
        verbose_name = "Lugar de fallecimiento"
        verbose_name_plural = "Lugares de fallecimiento"
