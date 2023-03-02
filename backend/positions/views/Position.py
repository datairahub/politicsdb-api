# -*- coding: utf-8 -*-
from core.viewsets import BaseModelViewSet
from positions import models, serializers, filters


class PositionViewSet(BaseModelViewSet):
    """
    Position Viewset

    :model:`positions.Position` management endpoint.
    """

    model = models.Position
    serializer_class = serializers.PositionListSerializer
    serializer_classes = {
        "retrieve": serializers.PositionRetrieveSerializer,
    }
    filterset_class = filters.PositionFilter
