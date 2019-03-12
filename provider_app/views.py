# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwars):
        try:
            user = User.objects.get(username=username)
            return user
        except:
            user = User.objects.create_user(username, username, "password")
            return user