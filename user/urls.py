from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import (
    UserRegistrationView,
    OTPVerificationView,
    LoginView,
    RequestOTPView,
    ResetPasswordView,
    EmployeProfileView,
    RecuiterProfileView,
    CompanyProfileView,
    WorkedCompaniesView
)
urlpatterns = [
    path('user-registration/', UserRegistrationView, name='user-registration'),
    path('otp-verification/',OTPVerificationView, name='account-verification'),
    path('login/', LoginView, name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-otp/', RequestOTPView, name='request-otp'),
    path('reset-password/', ResetPasswordView, name='reset-password'),
    
    path('profile/', EmployeProfileView.as_view(), name='employe-profile'),
    path('recuiter-profile/', RecuiterProfileView.as_view(), name='recuiter_profile'),
    path('worked-companies/', WorkedCompaniesView.as_view(), name='worked-companies'),
    path('company-profile/', CompanyProfileView.as_view(), name='company-profile'),
]
