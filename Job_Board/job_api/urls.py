from django.urls import path
from .views import (
    UserRegistrationView, UserLoginView, UserLogoutView,
    EmployerProfileView, ApplicantProfileView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("employer-profile/", EmployerProfileView.as_view(), name="employer-profile"),
    path("applicant-profile/", ApplicantProfileView.as_view(), name="applicant-profile"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
