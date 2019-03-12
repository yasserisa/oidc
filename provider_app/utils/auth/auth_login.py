# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
# Variables Settings
from django.conf import settings
# Extra Functions
import provider_app.utils.helpers.run_utils as run_utils
import provider_app.utils.helpers.utils as utils
import provider_app.utils.error.handle as error_handle
import provider_app.utils.helpers.logs as logs
from provider_app.responses import response
# Standard
import requests
import json
import re


@csrf_exempt
# Logout from other site
def logout_user(request):
    if request.method == "GET":
      return response().bad_method()
    logout(request)
    request.session.flush()
    # query string para URL de retorno o respuesta por default
    return redirect(request.GET.get("redirect")
                    if request.GET.get("redirect") is not None and
                    utils.validate_url(url)
                    else HttpResponse(
        json.dumps({"message": "Logout Success"}),
        content_type="application/json",
        status=204))

def login_user(request):
    # Se comprueba metodos HTTP
    if request.method == "GET" and request.method == "POST":
        return response().bad_method()
    # En caso de GET
    if request.GET:
        nombreApp = utils.name_client_id(str(request))
        get_response = \
        {
            "next": request.GET["next"],
            "nombreApp": nombreApp
        }
        return render(request,
                      "auth.html" if nombreApp is not None else "error.html",
                      get_response)
    # En caso de POST
    # run y Clave en formulario POST
    post_request = \
        {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
            "next": request.POST["next"],
            "nombreApp": request.POST["nombreApp"],
            "HTTP_USER_AGENT": request.META["HTTP_USER_AGENT"],
            "HTTP_X_FORWARDED_FOR": request.META["HTTP_X_FORWARDED_FOR"]
        }
    logs_data = post_request.copy()
    del logs_data["password"]
    logs_data["client_id"] = utils.client_id_session(request.POST["next"])
    # check post
    if not utils.check_body(post_request, settings.BODY_SCHEMA):
        logs["error"] = "request"
        logs.logs(logs_data)
        return render(request,
                      "auth.html",
                      {
                          "error": settings.RESPONSES_LOGIN["UNAUTHORIZED"],
                          "next": post_request["next"],
                          "nombreApp": post_request["nombreApp"]
                      })
    # Chequeamos run
    if not run_utils.check_run(request.POST.get("username")):
        logs_data["error"] = "RUN"
        logs.logs(logs_data)
        return render(request,
                      "auth.html",
                      {
                          "error": settings.RESPONSES_LOGIN["GENERIC"],
                          "next": post_request["next"],
                          "nombreApp": post_request["nombreApp"]
                      })

    numero_run, DV_run = run_utils.parse_run(request.POST.get("username"))
    # Logueamos en el sistema de Django
    user = authenticate(username=request.POST.get("username"),
                        password=request.POST.get("password"))
    # Login Sandbox
    if settings.SANDBOX:
        logs_data["error"] = None
        logs.logs(logs_data)
        login(request, user)
        return HttpResponseRedirect(post_request["next"])
    # Respuesta API IDENTITY SERVER
    response_auth = requests.post(settings.URL_AUTH,
                                  json={
                                      "numero": numero_run,
                                      "password": request.POST.get("password"),
                                      "token": settings.TOKEN_AUTH
                                  })
    if response_auth.status_code == 200 and response_auth.json()["code"] == 18:
        logs_data["error"] = None
        logs.logs(logs_data)
        login(request, user)
        return HttpResponseRedirect(post_request["next"])
    logs_data["error"] = response_auth.json()["code"]
    logs.logs(logs_data)
    return render(request,
                  "auth.html",
                  {
                      "error": settings.RESPONSES_LOGIN["GENERIC"],
                      "next": post_request["next"],
                      "nombreApp": post_request["nombreApp"]
                  })
