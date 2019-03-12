# -*- coding: utf-8 -*-
from oidc_provider.models import Client
import re
from jsonschema import validate
from django.utils.encoding import smart_str


def client_id(request):
    try:
        return re.findall("client_id%3D(.*?)%26?", request, re.DOTALL)[0]
    except:
        client_id = re.findall("client_id%3D(.*)", request, re.DOTALL)
        if len(client_id) > 0:
            return str(client_id[0]).strip(">").strip("'")
        else:
            return None

def name_client_id(request_GET):

    # Check Name App
    try:
        client_id_row = Client.objects.filter(client_id=client_id(request_GET)).values()[0]
        return smart_str(client_id_row["name"])
    except:
        return None

def client_id_session(request_POST):
    return client_id(request_POST)

def validate_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain
        r'localhost|' #localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None


def check_body(body, schema):
    try:
        validate(body, schema)
        return True
    except:
        return False, None
