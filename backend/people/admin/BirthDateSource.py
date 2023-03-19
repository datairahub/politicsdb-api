# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import DateSourceAdmin
from people.models import BirthDateSource, Person


class BirthDateSourceAdmin(DateSourceAdmin):
    model = BirthDateSource


admin.site.register(BirthDateSource, BirthDateSourceAdmin)
