# -*- coding: utf-8 -*-
import os
from .base import *

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-=y&no440e0zjaljtyi%zfpuk2_#dy%fs5f%sa(w_i)#@5wsys^",
)

DEBUG = True

ALLOWED_HOSTS = ["*"]

FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")

ADMIN_PATH = os.environ.get("ADMIN_PATH", "admin/")

DATABASES = {
    "default": {
        "NAME": os.environ.get("DB_NAME"),
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "HOST": os.environ.get("DB_HOST"),
        "USER": os.environ.get("DB_USER"),
        "PORT": os.environ.get("DB_PORT"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
    }
}
