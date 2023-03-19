# -*- coding: utf-8 -*-
from rest_framework.decorators import action
from rest_framework.response import Response
from core.viewsets import BaseModelViewSet

from positions import models, serializers
from positions.selectors.institutions import (
    get_institution_distribution_age_stats,
    get_institution_mean_age_stats,
    get_institution_genre_stats,
)


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

    @action(detail=True, methods=["get"])
    def stats_age_all(self, request, pk):
        """
        Return institution distribution age stats
        """
        return Response(get_institution_distribution_age_stats(pk, request.GET))

    @action(detail=True, methods=["get"])
    def stats_age_mean(self, request, pk):
        """
        Return institution mean age stats
        """
        return Response(get_institution_mean_age_stats(pk, request.GET))

    @action(detail=True, methods=["get"])
    def stats_genre(self, request, pk):
        """
        Return institution genre stats
        """
        return Response(get_institution_genre_stats(pk, request.GET))
