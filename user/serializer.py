from rest_framework import serializers
from user.models import CustomUser
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .utils import str_generator, number_generator
from QOK.settings import Redis_object


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('email is exist.')
        return value

    def save(self, **kwargs):
        request = self.context['request']
        email = self.validated_data['email']
        password = self.validated_data['password']
        rand_str = str_generator(10)
        Redis_object.set(email, f"{password}/{rand_str}", ex=3600)
        original_url = f"{email}/{rand_str}"
        encode_url = urlsafe_base64_encode(force_bytes(original_url))
        message = f"http://{get_current_site(request).domain}/user/verify?u={encode_url}"
        send_mail("Verify", message, 'faniamtest@gmail.com', [email])


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RestorePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('email is not exists.')
        return value

    def save(self, **kwargs):
        email = self.validated_data['email']
        rand_number = number_generator(5)
        Redis_object.set(email, rand_number, ex=900)
        message = f"Your code: {rand_number}"
        send_mail("Restore password", message, 'faniamtest@gmail.com', [email])


class RestorePasswordVerifySerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    code = serializers.CharField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('email is not exists.')
        return value

    def validate(self, attrs):
        email = attrs['email']
        rand_number_redis = Redis_object.get(email)
        if attrs['code'] != rand_number_redis:
            raise serializers.ValidationError('code is invalide.')
        return attrs

    def expire_code(self):
        email = self.validated_data['email']
        Redis_object.expire(email)

    def save(self, **kwargs):
        email = self.validated_data['email']
        password = self.validated_data['password']
        try:
            user = CustomUser.objects.get(email=email)
        except:
            user = None
        if user:
            user.set_password(password)
            user.save()
            self.expire_code()
            return user
