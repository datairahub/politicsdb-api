# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework import routers
from people import views

# fmt: off
router = routers.DefaultRouter()
router.register(r"person", views.PersonViewSet, basename="person")
# fmt: on

urlpatterns = [path("", include(router.urls))]
