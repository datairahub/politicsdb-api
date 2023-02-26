# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(settings.ADMIN_PATH, admin.site.urls),
    path(
        f"{settings.API_PATH}position/",
        include(("positions.urls", "position"), namespace="position"),
    ),
]
