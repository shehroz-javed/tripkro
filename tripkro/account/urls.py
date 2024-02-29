from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from account.views import UserRegisterView, VerifyUserEmailView, ForgetPasswordView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path(
        "verify-email/<str:token>/", VerifyUserEmailView.as_view(), name="verify-email"
    ),
    path("forget-password/", ForgetPasswordView.as_view(), name="forget-password"),
    # simple jwt views
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
]
