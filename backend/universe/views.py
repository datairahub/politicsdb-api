# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from universe.services.fields import get_models_fields_data


class UniverseFieldsViewSet(viewsets.ViewSet):
    """
    Universe Viewset (Constrains viewset)

    Views
        - list
    """

    permission_classes = (AllowAny,)

    def list(self, *args):
        return Response({"results": get_models_fields_data()})
