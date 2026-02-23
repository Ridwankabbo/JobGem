from django.urls import path
from .views import (
    UserRegistrationView,
    AccountVerificationView,
)
urlpatterns = [
    path('user-registration/', UserRegistrationView),
    path('account-verification/',AccountVerificationView),
]
