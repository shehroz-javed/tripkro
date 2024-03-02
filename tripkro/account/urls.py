from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from account.views import (
    UserRegisterView,
    VerifyUserEmailView,
    ForgetPasswordView,
    UserLoginView,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path(
        "verify-email/<str:token>/", VerifyUserEmailView.as_view(), name="verify-email"
    ),
    path("forget-password/", ForgetPasswordView.as_view(), name="forget-password"),
    # simple jwt views
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
]
