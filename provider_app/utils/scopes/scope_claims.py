# -*- coding: utf-8 -*-
import provider_app.utils.helpers.run_utils as utils
# OIDC_EXTRA_SCOPE_CLAIMS
from oidc_provider.lib.claims import ScopeClaims
from django.utils.translation import ugettext as _
import requests
from django.conf import settings
import json


class CustomScopeClaims(ScopeClaims):

    # Compatibilidad
    info_rut = (
        _(u"RUT"),
        _(u"Antiguo Scope"),
    )
    info_nombre = (
        _(u"nombre"),
        _(u"Antiguo Scope"),
    )
    # New
    info_run = (
        _(u"RUN"),
        _(u"Obtiene Rol Único Nacional de la persona que está accediendo"),
    )

    info_name = (
        _(u"nombre"),
        _(u"Obtiene los nombres y apellidos de la persona que está accediendo"),
    )

    info_email = (
        _(u"email"),
        _(u"Obtiene el email de la persona que está accediendo"),
    )

    info_phone = (
        _(u"phone"),
        _(u"Obtiene el teléfono de la persona que está accediendo"),
    )

    #Normalizados
    info_rolunico = (
        _(u"Rol Único"),
        _(u"Obtiene Rol Único Nacional de la persona que está accediendo"),
    )

    info_nombres = (
        _(u"nombres"),
        _(u"Obtiene los nombres y apellidos de la persona que está accediendo"),
    )

    info_correo = (
        _(u"correo"),
        _(u"Obtiene el email de la persona que está accediendo"),
    )

    info_telefono = (
        _(u"phone"),
        _(u"Obtiene el teléfono de la persona que está accediendo"),
    )

    # Compatibilidad
    def scope_rut(self):

        try:
            run = str(self.user)
            numero, DV = utils.parse_run(run)
            dic = {}
            dic["RUT"] = "{:,}".format(numero).replace(",", ".") + "-" + DV
        except:
            return response().internal_error()
        return dic


    def scope_nombre(self):

        try:
            run = str(self.user)
            numero, DV = utils.parse_run(run)
            if settings.SANDBOX:
                dic = {}
                dic["nombres"] = "Maria Carmen De los angeles"
                dic["apellidoPaterno"] = "Del rio"
                dic["apellidoMaterno"] = "Gonzalez"
                dic["RUT"] = "{:,}".format(numero).replace(",", ".") + "-" + DV
                return dic
            data_json = {}
            data_json["token"] = str(settings.TOKEN_AUTH)
            data_json["numero"] = numero
            data_user = requests.post(settings.URL_GET_INFO_USER, json=data_json)
            data_user = json.loads(data_user.text)["object"]
            dic = {}
            dic["nombres"] = " ".join(data_user["name"]["nombres"])
            dic["apellidoPaterno"] = " ".join(data_user["name"]["apellidos"])
            dic["apellidoMaterno"] = " "
            dic["RUT"] = "{:,}".format(numero).replace(",", ".") + "-" + DV
        except:
            return response().internal_error()
        return dic

    # New
    def scope_run(self):

        try:
            run = str(self.user)
            numero, DV = utils.parse_run(run)
            dic = {}
            dic["RolUnico"] = {"numero": numero, "DV": DV, "tipo": "RUN"}
        except:
            return response().internal_error()
        return dic

    def scope_name(self):

        try:
            run = str(self.user)
            numero, DV = utils.parse_run(run)
            if settings.SANDBOX:
                dic = {}
                dic["name"] = {}
                dic["name"]["nombres"] = ["Maria", "Carmen", "De los angeles"]
                dic["name"]["apellidos"] = ["Del rio", "Gonzalez"]
                dic["RolUnico"] = {"numero": numero, "DV": DV, "tipo": "RUN"}
                return dic
            data_json = {}
            data_json["token"] = str(settings.TOKEN_AUTH)
            data_json["numero"] = numero
            data_user = requests.post(settings.URL_GET_INFO_USER, json=data_json)
            data_user = json.loads(data_user.text)["object"]
            try:
                del data_user["other_info"]
            except:
                pass
        except:
            return response().internal_error()
        return data_user

    def scope_email(self):

        try:
            run = str(self.user)
            numero, DV = utils.parse_run(run)
            if settings.SANDBOX:
                dic = {}
                dic["name"] = {}
                dic["name"]["nombres"] = ["Maria", "Carmen", "De los angeles"]
                dic["name"]["apellidos"] = ["Del rio", "Gonzalez"]
                dic["RolUnico"] = {"numero": numero, "DV": DV, "tipo": "RUN"}
                dic["email"] = "mcdla@mail.com"
                return dic
            data_json = {}
            data_json["token"] = str(settings.TOKEN_AUTH)
            data_json["numero"] = numero
            data_user = requests.post(settings.URL_GET_INFO_USER, json=data_json)
            try:
                return {"email": json.loads(data_user.text)["object"]["other_info"]["email"]}
            except:
                return {"email": "None"}
        except:
            return response().internal_error()

    def scope_phone(self):

        try:
            run = str(self.user)
            numero, DV = utils.parse_run(run)
            if settings.SANDBOX:
                dic = {}
                dic["name"] = {}
                dic["name"]["nombres"] = ["Maria", "Carmen", "De los angeles"]
                dic["name"]["apellidos"] = ["Del rio", "Gonzalez"]
                dic["RolUnico"] = {"numero": numero, "DV": DV, "tipo": "RUN"}
                return dic
            data_json = {}
            data_json["token"] = str(settings.TOKEN_AUTH)
            data_json["numero"] = numero
            data_user = requests.post(settings.URL_GET_INFO_USER, json=data_json)
            try:
                return {"phone": json.loads(data_user.text)["object"]["other_info"]["phone"]}
            except:
                return {"phone": "None"}
        except:
            return response().internal_error()

    def scope_rolunico(self):

        try:
            run = str(self.user)
            numero, DV = utils.parse_run(run)
            dic = {}
            dic["rolUnico"] = {"numero": numero, "dv": DV, "tipo": "Nacional"}
        except:
            return response().internal_error()
        return dic

    def scope_nombres(self):

        try:
            run = str(self.user)
            numero, DV = utils.parse_run(run)
            if settings.SANDBOX:
                dic = {}
                dic["name"] = {}
                dic["name"]["nombres"] = ["Maria", "Carmen", "De los angeles"]
                dic["name"]["apellidos"] = ["Del rio", "Gonzalez"]
                return dic
            data_json = {}
            data_json["token"] = str(settings.TOKEN_AUTH)
            data_json["numero"] = numero
            data_user = requests.post(settings.URL_GET_INFO_USER, json=data_json).json()["object"]["name"]
        except:
            return response().internal_error()
        return data_user

    def scope_correo(self):

        try:
            run = str(self.user)
            numero, DV = utils.parse_run(run)
            if settings.SANDBOX:
                dic = {}
                dic["name"] = {}
                dic["name"]["nombres"] = ["Maria", "Carmen", "De los angeles"]
                dic["name"]["apellidos"] = ["Del rio", "Gonzalez"]
                dic["rolUnico"] = {"numero": numero, "dv": DV, "tipo": "Nacional"}
                dic["email"] = "mcdla@mail.com"
                return dic
            data_json = {}
            data_json["token"] = str(settings.TOKEN_AUTH)
            data_json["numero"] = numero
            data_user = requests.post(settings.URL_GET_INFO_USER, json=data_json)
            try:
                return {"email": json.loads(data_user.text)["object"]["other_info"]["email"]}
            except:
                return {"email": "None"}
        except:
            return response().internal_error()

    def scope_telefono(self):

        try:
            run = str(self.user)
            numero, DV = utils.parse_run(run)
            if settings.SANDBOX:
                dic = {}
                dic["name"] = {}
                dic["name"]["nombres"] = ["Maria", "Carmen", "De los angeles"]
                dic["name"]["apellidos"] = ["Del rio", "Gonzalez"]
                dic["rolUnico"] = {"numero": numero, "dv": DV, "tipo": "Nacional"}
                return dic
            data_json = {}
            data_json["token"] = str(settings.TOKEN_AUTH)
            data_json["numero"] = numero
            data_user = requests.post(settings.URL_GET_INFO_USER, json=data_json)
            try:
                return {"phone": json.loads(data_user.text)["object"]["other_info"]["phone"]}
            except:
                return {"phone": "None"}
        except:
            return response().internal_error()