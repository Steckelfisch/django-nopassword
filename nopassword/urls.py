# -*- coding: utf8 -*-
from django.conf.urls import url
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from nopassword import views

urlpatterns = [
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^login/code$', views.LoginCodeView.as_view(), name='login_code'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    url('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
