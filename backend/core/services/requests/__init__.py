# -*- coding: utf-8 -*-
import zlib
import base64
from urllib import request, parse


def request_page(url, data=None, headers={}):
    """
    Get page html from url
    """
    if data:
        data = parse.urlencode(data).encode()

    req = request.Request(url, data, headers)
    response = request.urlopen(req, timeout=30)

    if response.info().get("Content-Encoding") == "gzip":
        reqdata = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)
        # reqdata = gzip.decompress(response.read())
    else:
        reqdata = response.read()

    return reqdata


def request_page_b64(url, data=None, headers={}):
    """
    Get page base64 from url
    """
    return base64.b64encode(request_page(url, data, headers))
