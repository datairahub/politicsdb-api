# -*- coding: utf-8 -*-
import uuid
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse


def json_default_field():
    return {}


class BaseAbstracModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    metadata = models.JSONField(default=json_default_field)

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(
            "admin:%s_%s_change" % (content_type.app_label, content_type.model),
            args=(self.id,),
        )

    class Meta:
        abstract = True


class CategoryAbstractModel(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.name

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(
            "admin:%s_%s_change" % (content_type.app_label, content_type.model),
            args=(self.id,),
        )

    class Meta:
        abstract = True
