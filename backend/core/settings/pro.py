# -*- coding: utf-8 -*-
import os
from .base import *

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = [os.environ.get("FRONTEND_URL")]

FRONTEND_URL = os.environ.get("FRONTEND_URL")

ADMIN_PATH = os.environ.get("ADMIN_PATH")
