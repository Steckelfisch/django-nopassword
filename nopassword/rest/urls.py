# -*- coding: utf-8 -*-
from django.conf.urls import url

from nopassword.rest import views

urlpatterns = [
    url('login', views.LoginView.as_view(), name='rest_login'),
    url('login/code', views.LoginCodeView.as_view(), name='rest_login_code'),
    url('logout', views.LogoutView.as_view(), name='rest_logout'),
]
