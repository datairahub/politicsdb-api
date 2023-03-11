# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from core.services.dump import dump_data


@login_required
def dump(request):
    dump_data()
    return JsonResponse({"ok": 200})
