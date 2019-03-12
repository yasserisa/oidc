# -*- coding: utf-8 -*-
from django.http import HttpResponse
import json

    
class response:

    def __init__(self):
        pass

    # Generic
    def bad_method(self):
        message = {"error": "Bad method"}
        return HttpResponse(json.dumps(message), content_type="application/json", status=405)

    def bad_request(self):
        message = {"error": "Bad request"}
        return HttpResponse(json.dumps(message), content_type="application/json", status=400)

    def internal_error(self):
        message = {"error": "Error interno, por favor intente más tarde"}
        return HttpResponse(json.dumps(message), content_type="application/json", status=500)

    def unauthorized(self):
        message = {"error": "Usuario no autorizado para realizar esta acción"}
        return HttpResponse(json.dumps(message), content_type="application/json", status=401)

    def unavailable(self):
        message = {"error": "Temporalmente fuera de servicio, por favor intente más tarde"}
        return HttpResponse(json.dumps(message), content_type="application/json", status=503)
