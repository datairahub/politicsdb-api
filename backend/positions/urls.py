# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework import routers
from positions import views

# fmt: off
router = routers.DefaultRouter()
router.register(r"institution", views.InstitutionViewSet, basename="institution")
# fmt: on

urlpatterns = [path("", include(router.urls))]
