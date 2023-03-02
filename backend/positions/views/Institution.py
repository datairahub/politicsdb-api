# -*- coding: utf-8 -*-
from core.viewsets import BaseModelViewSet
from positions import models, serializers


class InstitutionViewSet(BaseModelViewSet):
    """
    Institution Viewset

    :model:`positions.Institution` management endpoint.
    """

    model = models.Institution
    serializer_class = serializers.InstitutionListSerializer
    serializer_classes = {
        "retrieve": serializers.InstitutionRetrieveSerializer,
    }
    filterset_fields = ("adm0",)
