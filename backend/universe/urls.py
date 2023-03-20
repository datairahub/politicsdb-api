# -*- coding: utf-8 -*-
from django.urls import path
from django.urls import include
from rest_framework import routers
from universe import views

router = routers.DefaultRouter()
router.register(r"fields", views.UniverseFieldsViewSet, basename="universe")

urlpatterns = [path("", include(router.urls))]
