# -*- coding: utf-8 -*-
import os
from .base import *

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-=y&no440e0zjaljtyi%zfpuk2_#dy%fs5f%sa(w_i)#@5wsys^",
)

DEBUG = True

ALLOWED_HOSTS = ["*"]
