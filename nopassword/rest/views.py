# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from nopassword.rest import serializers
from nopassword.rest.exceptions import UserNotValid


class LoginView(GenericAPIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Inject remote IP address into data
        data = request.data
        local_ip_used = request.headers.get("local-ip-used", '127.0.0.1')
        data['remote_ip'] = request.headers.get("X-Forwarded-For", local_ip_used)

        try:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except UserNotValid:
            # We ignore this type of exceptions
            pass

        return Response(
            {"detail": _("Login code has been sent.")},
            status=status.HTTP_200_OK
        )


@method_decorator(sensitive_post_parameters('code'), 'dispatch')
class LoginCodeView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.LoginCodeSerializer

    def process_login(self):
        django_login(self.request, self.user)

    def login(self):
        self.user = self.serializer.validated_data['user']
        self.tokens = RefreshToken.for_user(self.user)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

    def get_response(self):
        data = {
            'access': str(self.tokens.access_token),
            'refresh': str(self.tokens),
            'next': self.serializer.validated_data['user'].login_code.next,
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        self.serializer.save()
        self.login()
        return self.get_response()


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        django_logout(request)

        return Response(
            {"detail": _("Successfully logged out.")},
            status=status.HTTP_200_OK,
        )
