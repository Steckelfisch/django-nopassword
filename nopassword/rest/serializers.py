# -*- coding: utf-8 -*-
import json
from urllib.parse import urlencode
from urllib.request import urlopen
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.conf import settings
from nopassword import forms


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    recaptcha_token = serializers.CharField()
    remote_ip = serializers.CharField()
    next = serializers.CharField(required=False, allow_null=True)

    form_class = forms.LoginForm

    def validate(self, data):
        # Validate reCaptcha
        if settings.RECAPTCHA_URI and settings.RECAPTCHA_PRIVATE:
            params = urlencode({
                'secret': f"{settings.RECAPTCHA_PRIVATE}",
                'response': data['recaptcha_token'],
                'remote_ip': data['remote_ip'],
            })

            data = urlopen(settings.RECAPTCHA_URI, params.encode('utf-8')).read()
            result = json.loads(data)
            success = result.get('success', None)

            if not success:
                raise serializers.ValidationError({'recaptcha': 'Invalid reCaptcha'})

        self.form = self.form_class(data=self.initial_data)

        if not self.form.is_valid():
            raise serializers.ValidationError(self.form.errors)

        return self.form.cleaned_data

    def save(self):
        request = self.context.get('request')
        return self.form.save(request=request)


class LoginCodeSerializer(serializers.Serializer):
    code = serializers.CharField()

    form_class = forms.LoginCodeForm

    def validate(self, data):
        request = self.context.get('request')

        self.form = self.form_class(data=self.initial_data, request=request)

        if not self.form.is_valid():
            raise serializers.ValidationError(self.form.errors)

        return self.form.cleaned_data

    def save(self):
        self.form.save()


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('key',)
