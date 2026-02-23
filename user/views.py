from django.shortcuts import render
from rest_framework.decorators import APIView, api_view
from rest_framework.response import Response
from .models import User
from .serializer import (
    UserRegistrationSerializer,
    AccountVerificationByOtpSerializer,
)
# Create your views here.

""" 
    ================================
        USER REGISTRATION VIEW   
    ================================
"""
@api_view(['POST'])
def UserRegistrationView(request):
    serializer = UserRegistrationSerializer(request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

""" 
    ================================
        VERIFICATION OTP VIEW   
    ================================
"""
@api_view(['POST'])
def AccountVerificationView(request):
    serializer = AccountVerificationByOtpSerializer(request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        otp = serializer.validated_data.get('otp')
        try: 
            user = User.objects.get(email = email)
            if user.otp == otp:
                user.is_active = True
                user.otp = None
                user.save()
                
                return Response({
                    "response":"Account successfully verified"
                })
        except User.DoesNotExist:
            return Response({
                "response":"User doesn't found"
            })
    


    
