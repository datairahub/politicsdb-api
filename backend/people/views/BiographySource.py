# -*- coding: utf-8 -*-
from core.viewsets import BaseModelViewSet
from people import models, serializers


class BiographySourceViewSet(BaseModelViewSet):
    """
    BiographySource Viewset

    :model:`people.BiographySource` management endpoint.
    """

    model = models.BiographySource
    serializer_class = serializers.BiographySourceListSerializer
    filterset_fields = ("person",)
