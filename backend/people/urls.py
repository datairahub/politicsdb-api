# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework import routers
from people import views

# fmt: off
router = routers.DefaultRouter()
router.register(r"person",          views.PersonViewSet,          basename="person")
router.register(r"birthdatesource", views.BirthDateSourceViewSet, basename="birthdatesource")
router.register(r"biographysource", views.BiographySourceViewSet, basename="biographysource")
# fmt: on

urlpatterns = [path("", include(router.urls))]
