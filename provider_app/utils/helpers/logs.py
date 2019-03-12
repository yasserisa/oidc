# -*- coding: utf-8 -*-
import requests
import json
import datetime
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
import socket


# LOGS
def logs(request):
    g = GeoIP2()
    try:
        country = str(g.city(ipaddr_remote)['country_code'])
    except:
        country = None
    request["country"] = country
    request["datetime"] = str(datetime.datetime.utcnow())
    # Collection to insert mongodb
    request["collection"] = "logs_oidc"
    if settings.SANDBOX:
        request["collection"] = "logs_oidc_sandbox"
    # UDP Socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(0.1)
    addr = ("127.0.0.1", settings.PORT_UDP_LOGS)
    client_socket.sendto(json.dumps(request).encode("utf-8"), addr)