from django.urls import path
from .views import (
    UserRegistrationView,
    OTPVerificationView,
    LoginView,
    RequestOTPView,
    ResetPasswordView
)
urlpatterns = [
    path('user-registration/', UserRegistrationView, name='user-registration'),
    path('otp-verification/',OTPVerificationView, name='account-verification'),
    path('login/', LoginView, name='login'),
    path('request-otp/', RequestOTPView, name='request-otp'),
    path('reset-password/', ResetPasswordView, name='reset-password')
]
