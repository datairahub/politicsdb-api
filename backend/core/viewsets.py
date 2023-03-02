# -*- coding: utf-8 -*-
from django.conf import settings
from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import AllowAny
from django_filters import rest_framework as rf_filters


def get_error_headers() -> dict:
    """
    Get headers for erroneous responses
    """
    return {
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Headers": (
            "Authorization,"
            "Accept,"
            "Origin,"
            "DNT,"
            "X-CustomHeader,"
            "Keep-Alive,"
            "User-Agent,"
            "X-Requested-With,"
            "If-Modified-Since,"
            "Cache-Control,"
            "Content-Type,"
            "Content-Range,"
            "Range,"
            "X-CSRF-Token,"
            "Access-Control-Request-Headers"
        ),
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS,PUT,DELETE,PATCH",
        "Access-Control-Allow-Origin": settings.FRONTEND_URL,
    }


class BaseModelViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    permission_classes = (AllowAny,)
    filter_backends = (rf_filters.DjangoFilterBackend, filters.OrderingFilter)

    def get_serializer_class(self):
        try:
            return self.serializer_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        self.pagination_class.max_page_size = settings.REST_FRAMEWORK.get(
            "MAX_PAGE_SIZE", 100
        )
        self.pagination_class.page_size = int(
            self.request.GET.get(
                "page_size", settings.REST_FRAMEWORK.get("PAGE_SIZE", 10)
            )
        )
        return self.model.objects.all()

    def finalize_response(self, request, *args, **kwargs):
        response = super().finalize_response(request, *args, **kwargs)
        if response.status_code >= 300:
            for item in get_error_headers().items():
                response[item[0]] = item[1]
        return response
