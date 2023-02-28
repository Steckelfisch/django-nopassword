# -*- coding: utf8 -*-
from django.urls import include, re_path

from nopassword import views

urlpatterns = [
    re_path(r'^login$', views.LoginView.as_view(), name='login'),
    re_path(r'^login/code$', views.LoginCodeView.as_view(), name='login_code'),
    re_path(r'^logout$', views.LogoutView.as_view(), name='logout'),
]
