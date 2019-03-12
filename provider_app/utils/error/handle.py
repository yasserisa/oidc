# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
import json


# Catch error 500
def catch_error_500(request):
    return HttpResponseRedirect("https://www.claveunica.gob.cl/error500")


# Catch error 404
def catch_error_404(request):
    return HttpResponseRedirect("https://www.claveunica.gob.cl/error404")


# Catch error 500
def missing_csrf(request, reason):
    mensaje = {"message": str(reason)}
    return HttpResponse(json.dumps(mensaje), content_type="application/json", status=401)   
