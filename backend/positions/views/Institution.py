# -*- coding: utf-8 -*-
from core.viewsets import BaseModelViewSet
from positions import models, serializers


class InstitutionViewSet(BaseModelViewSet):
    """
    Institution Viewset

    :model:`positions.Institution` management endpoint.
    """

    model = models.Institution
    serializer_class = serializers.InstitutionSerializer
    filterset_fields = ("adm0",)
