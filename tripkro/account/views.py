from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from account.serializers import (
    UserRegisterSerializer,
    ResetPasswordSerializer,
    UserLoginSerializer,
    UserSerializer,
)
from account.utils import send_email_verify_mail, get_tokens_for_user

from tripkro.utils import CustomErrorSerializer, decode_token, encode_token


User = get_user_model()
error = CustomErrorSerializer()


class UserRegisterView(APIView):
    def post(self, request):

        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data["is_active"] = False
            email = serializer.validated_data.get("email")
            send_email_verify_mail(email)
            serializer.save()

            return Response(
                {
                    "status": 201,
                    "message": "Your account has been registered successfully. Please verify your email to activate your account.",
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "status": 400,
                "error": error.to_representation(serializer.errors),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserLoginView(APIView):
    def post(self, request):

        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            user = User.objects.filter(email=email).first()
            if not user:
                return Response(
                    {"status": 404, "error": ["User with this email does not exist"]},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if not check_password(password, user.password):
                return Response(
                    {"status": 404, "error": ["Incorrect password"]},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if not user.is_email_verified:
                return Response(
                    {
                        "status": 401,
                        "error": ["Kindly verify your email first to procced"],
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            if not user.is_active:
                return Response(
                    {
                        "status": 400,
                        "error": [
                            "Your account in deactivated .Contact us if you want to activate your account"
                        ],
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            user_data = UserSerializer(user).data
            token = get_tokens_for_user(user)
            return Response(
                {
                    "status": 200,
                    "message": "Login successfully",
                    "data": {
                        "access": token["access"],
                        "refresh": token["refresh"],
                        "user": user_data,
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"status": 400, "error": error.to_representation(serializer.errors)},
            status=status.HTTP_400_BAD_REQUEST,
        )


class VerifyUserEmailView(APIView):
    def get(self, request, token):

        if not token:
            return HttpResponse("Something went wrong kindly try again after some time")

        try:
            decode_data = decode_token(token)
            user = User.objects.get(email=decode_data["email"])
            if user.is_email_verified:
                return HttpResponse("Email already verified")

            user.is_email_verified = True
            user.is_active = True
            user.save()
            return HttpResponse("Email verified successfully")

        except User.DoesNotExist:
            return HttpResponse("User not found")

        except Exception as e:
            return HttpResponse(f"Error : {e.args}")


class ForgetPasswordView(APIView):
    def get(self, request):

        email = request.query_params.get("email")

        if not email:
            return Response(
                {"status": 400, "error": "Kindly provide and email"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email, is_active=True)

            payload = {
                "email": user.email,
                "exp": timezone.now() + timezone.timedelta(minutes=30),
            }
            token = encode_token(payload)

            return Response(
                {
                    "status": 200,
                    "message": "The token will expire in 10 minutes",
                    "data": {"token": token},
                },
                status=status.HTTP_200_OK,
            )

        except User.DoesNotExist as e:
            return Response(
                {"status": 404, "error": e.args},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {
                    "status": 500,
                    "error": e.args,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):

        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():

            decode_data = decode_token(serializer.validated_data.get("token"))
            user = User.objects.get(email=decode_data["email"], is_active=True)

            password = serializer.validated_data.get("password")
            user.set_password(password)
            user.save()
            return Response(
                {"status": 200, "message": "password updated successfully"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "status": 400,
                "error": error.to_representation(serializer.errors),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
