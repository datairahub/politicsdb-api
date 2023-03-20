# -*- coding: utf-8 -*-
import uuid
from django.contrib.gis.db import models
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Identificador único de la instancia del modelo",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, null=False, help_text="Fecha de creación de la instancia"
    )
    updated_at = models.DateTimeField(
        auto_now=True, null=False, help_text="Última actualización de la instancia"
    )

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(
            "admin:%s_%s_change" % (content_type.app_label, content_type.model),
            args=(self.id,),
        )

    class Meta:
        abstract = True
        ordering = ("id",)
