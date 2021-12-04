from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import authenticate, login


class Userlog_Serializers(serializers.Serializer):
    username = serializers.CharField(max_length=150, min_length=2)
    password = serializers.CharField(max_length=65, min_length=8)

    class Meta:
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        username = attrs["username"]
        password = attrs["password"]
        self.user_cache = authenticate(self.request,
                                       username=username,
                                       password=password)
        if self.user_cache is None:
            raise serializers.ValidationError(_('Check your credentials'),
                                              code='auth_error',)
        return super().validate(attrs)


class User_Serializers(serializers.ModelSerializer):
    password_1 = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    password_2 = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    #username = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=255, min_length=4)
    first_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password_1', 'password_2']

    def validate(self, attrs):
        email = attrs['email']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(_('The email already is in use'),
                                              code='email_used',)
        elif attrs["password_2"] and attrs["password_1"] and attrs["password_1"] != attrs["password_2"]:
            raise serializers.ValidationError(_('The two password fields didn’t match.'),
                                              code='password_mismatch',)
        __ = attrs.pop("password_1")
        attrs['password'] = attrs.pop("password_2")
        attrs['is_superuser'] = False
        attrs['is_staff'] = False
        return super().validate(attrs)

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
