# -*- coding: utf-8 -*-
from core.viewsets import BaseModelViewSet
from positions import models, serializers


class PeriodViewSet(BaseModelViewSet):
    """
    Period Viewset

    :model:`positions.Period` management endpoint.
    """

    model = models.Period
    serializer_class = serializers.PeriodListSerializer
    serializer_classes = {
        "retrieve": serializers.PeriodRetrieveSerializer,
    }
    filterset_fields = ("institution",)
