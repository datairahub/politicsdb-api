# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from core.models import BaseModel


def json_default_field():
    return {}


class BaseAbstractModel(BaseModel):
    metadata = models.JSONField(
        default=json_default_field,
    )

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(
            "admin:%s_%s_change" % (content_type.app_label, content_type.model),
            args=(self.id,),
        )

    class Meta(BaseModel.Meta):
        abstract = True
