# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url
from provider_app.utils.auth.auth_login import logout_user, login_user
from oidc_provider.views import *

urlpatterns = [
    url(r"^accounts/login/$", login_user, name="login_user"),
    url(r"^api/v1/accounts/logout$", logout_user, name="logout_user"),
    url(r"^openid/", include("oidc_provider.urls", namespace=("oidc_provider"))),
    url(r"^openid/\.well-known/openid-configuration/$", ProviderInfoView.as_view(), name="provider_info"),
]

handler500 = "provider_app.utils.error.handle.catch_error_500"
