# -*- coding: utf-8 -*-
from django.urls import path
from . import views

# fmt: off
urlpatterns = [
  path('dump/', views.dump, name='dump'),
  path('clear_cache/', views.clear_cache, name='clear_cache'),
]
