from typing import Any, Dict
from django.contrib.auth import get_user_model

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "password2",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        password = data.get("password")
        password2 = data.pop("password2")

        if password != password2:
            raise serializers.ValidationError(
                "password and confirm password does not match"
            )
        return super().validate(data)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, data):

        data = super().validate(data)
        user = self.user
        refresh = self.get_token(user)
        user_data = UserSerializer(user).data

        data = {
            "user_data": user_data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return data
