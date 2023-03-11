# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# fmt: off
urlpatterns = [
    path(f"{settings.ADMIN_PATH}ext/", include(("admin_extension.urls", "adminext"), namespace="adminext")),
    path(settings.ADMIN_PATH, admin.site.urls),

    path(f"{settings.API_PATH}position/",   include(("positions.urls", "position"),   namespace="position")),
    path(f"{settings.API_PATH}people/",     include(("people.urls",    "people"),     namespace="people")),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# fmt: on
