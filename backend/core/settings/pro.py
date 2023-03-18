# -*- coding: utf-8 -*-
import os
from .base import *

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = [os.environ.get("FRONTEND_URL")]

FRONTEND_URL = os.environ.get("FRONTEND_URL")

ADMIN_PATH = os.environ.get("ADMIN_PATH")

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
