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
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=False,
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
