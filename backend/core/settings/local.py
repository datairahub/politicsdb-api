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
