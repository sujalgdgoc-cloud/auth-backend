from django.urls import path, include
from .views import UserRegisterView, UserLoginView, UserProfileView, UserChangePasswordView, UserResetPasswordView, ResetPasswordView
from rest_framework import generics

urlpatterns = [
    path("register/", UserRegisterView.as_view()),
    path("login/", UserLoginView.as_view()), 
    path("profile/", UserProfileView.as_view()),
    path("change-password/", UserChangePasswordView.as_view()),
    path("reset-password/", UserResetPasswordView.as_view()),
     path("forgot-password/", ResetPasswordView.as_view(), name="reset-password"),
]