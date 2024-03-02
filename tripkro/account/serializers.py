from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):

    c_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "term_condition",
            "password",
            "c_password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        password = data.get("password")
        password2 = data.pop("c_password")
        term_condition = data.get("term_condition", False)

        if password != password2:
            raise serializers.ValidationError(
                {"password": "password and confirm password does not match"}
            )

        if not term_condition:
            raise serializers.ValidationError(
                {
                    "term_condition": "You must check the term condition to create the account"
                }
            )
        return super().validate(data)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "full_name",
            "username",
            "email",
            "phone",
            "term_condition",
            "is_email_verified",
        )


class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, data):

#         data = super().validate(data)
#         user = self.user
#         refresh = self.get_token(user)
#         user_data = UserSerializer(user).data

#         data = {
#             "status": 200,
#             "data": {
#                 "refresh": str(refresh),
#                 "access": str(refresh.access_token),
#                 "user": user_data,
#             },
#         }
#         return data


class ResetPasswordSerializer(serializers.Serializer):

    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    c_password = serializers.CharField(required=True)

    def validate(self, data):
        password = data.get("password")
        c_password = data.pop("c_password")

        if not password or not c_password:
            raise serializers.ValidationError({"password": "Both fields are required"})

        if password != c_password:
            raise serializers.ValidationError(
                {"password": "Password and confirm password must be same"}
            )

        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({"password": [e for e in e]})

        return super().validate(data)
