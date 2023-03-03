# -*- coding: utf-8 -*-
from core.viewsets import BaseModelViewSet
from people import models, serializers


class BirthDateSourceViewSet(BaseModelViewSet):
    """
    BirthDateSource Viewset

    :model:`people.BirthDateSource` management endpoint.
    """

    model = models.BirthDateSource
    serializer_class = serializers.BirthDateSourceListSerializer
    filterset_fields = ("person",)
