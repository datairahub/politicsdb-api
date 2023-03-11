# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.cache import cache

from core.services.dump import dump_data


@login_required
def dump(request):
    dump_data()
    return JsonResponse({"dump_data": "ok"})


@login_required
def clear_cache(request):
    cache.clear()
    return JsonResponse({"clear_cache": "ok"})
