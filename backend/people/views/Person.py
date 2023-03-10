# -*- coding: utf-8 -*-
from core.viewsets import BaseModelViewSet
from people import models, serializers, filters


class PersonViewSet(BaseModelViewSet):
    """
    Person Viewset

    :model:`people.Person` management endpoint.
    """

    model = models.Person
    serializer_class = serializers.PersonListSerializer
    serializer_classes = {
        "retrieve": serializers.PersonRetrieveSerializer,
    }
    filterset_class = filters.PersonFilter
