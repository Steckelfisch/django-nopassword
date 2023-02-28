# -*- coding: utf-8 -*-
from django.urls import include, re_path

from nopassword.rest import views

urlpatterns = [
    re_path('login/code', views.LoginCodeView.as_view(), name='rest_login_code'),
    re_path('login', views.LoginView.as_view(), name='rest_login'),
    re_path('logout', views.LogoutView.as_view(), name='rest_logout'),
]
