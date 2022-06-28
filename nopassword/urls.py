# -*- coding: utf8 -*-
from django.conf.urls import url
from refreshtoken.routers import urlpatterns as rt_urlpatterns

from nopassword import views

urlpatterns = [
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^login/code$', views.LoginCodeView.as_view(), name='login_code'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
] + rt_urlpatterns
