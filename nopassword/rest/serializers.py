# -*- coding: utf-8 -*-
import json
from urllib.parse import urlencode
from urllib.request import urlopen
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from nopassword import forms


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    recaptcha_token = serializers.CharField()
    next = serializers.CharField(required=False, allow_null=True)

    form_class = forms.LoginForm

    def validate(self, data):
        # Validate reCaptcha
        URIReCaptcha = 'https://www.google.com/recaptcha/api/siteverify'
        private_recaptcha = '6Lec01MgAAAAACNe3aYAbruNVTk3BaWP39rN5wsf'
        recaptcha_token = data['recaptchaToken']
        remote_ip = '127.0.0.1'
        params = urlencode({
            'secret': private_recaptcha,
            'response': recaptcha_token,
            'remote_ip': remote_ip,
        })

        data = urlopen(URIReCaptcha, params.encode('utf-8')).read()
        result = json.loads(data)
        success = result.get('success', None)

        if not success:
            raise serializers.ValidationError('Invalid reCaptcha')
        else:
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
