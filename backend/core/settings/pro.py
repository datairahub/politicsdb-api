# -*- coding: utf-8 -*-
import os
from .base import *

SECRET_KEY = SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = []
