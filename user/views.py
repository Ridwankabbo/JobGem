from django.shortcuts import render
from rest_framework.decorators import APIView, api_view
from rest_framework.response import Response
from .models import User
from .serializer import (
    UserRegistrationSerializer,
    OTPVerificationSerializer,
    ResetPasswordSerializer,
)
from .utils import OtpManagement, send_otp_mail
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
# Create your views here.

""" 
    ================================
        USER REGISTRATION VIEW   
    ================================
"""
@api_view(['POST'])
def UserRegistrationView(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"response":"Account created successfully, Otp sended to you email. please check to verifi account"})
    return Response(serializer.errors)

""" 
    ================================
        REQUEST OTP VIEW   
    ================================
"""
@api_view(['POST'])
def RequestOTPView(request):
    email = request.data.get('email')
    purpose = request.data.get('purpose')
    otp_management = OtpManagement
    if not email and not purpose:
        return Response({"response":"Both email and password required"})
    
    otp = otp_management.GenerateOTP()
    otp_management.store_otp(email=email, otp=otp, purpose=purpose)
    # send_otp_mail(email, otp, purpose)
    print(f"{purpose} otp: {otp}")
    return Response({
        "response": f"OTP send to you {email} for {purpose}"
        })

""" 
    ================================
        VERIFICATION OTP VIEW   
    ================================
"""
@api_view(['POST'])
def OTPVerificationView(request):
    serializer = OTPVerificationSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        otp = serializer.validated_data.get('otp')
        purpose = serializer.validated_data.get('purpose')
                
        if not OtpManagement.verifi_otp(email, otp, purpose):
            return Response({"response":"Invalid otp"}, status=status.HTTP_400_BAD_REQUEST)
        if purpose == 'singup':
            try:
                user = User.objects.get(email=email)
                user.is_active = True
                user.save()
            except User.DoesNotExist:
                return Response({
                    "response":"User not found"
                }, status=status.HTTP_404_NOT_FOUND)
            return Response({
                    "response":"OTP verified successfull"
                }, status=status.HTTP_200_OK)
        if purpose == 'password_reset':
            return Response({
                "message":"OTP verified successfull, now you can reset you password",
                "email ": f"{email}"
            }, status=status.HTTP_200_OK)
        return Response(serializer.data)
    return Response(serializer.errors)

""" 
    ================================
        LOGIN VIEW   
    ================================
"""
@api_view(['POST'])
def LoginView(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response("Email and password are required", status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"response":"User doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
    if not user.check_password(password):
        return Response({'response':'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not user.is_active:
        return Response({"response":"Account isn't verified"}, status=status.HTTP_400_BAD_REQUEST)
    
    refresh = RefreshToken.for_user(user)
    return Response({
        "response":"Login successfully",
        "id":user.id,
        "refresh":str(refresh),
        "access":str(refresh.access_token)
    }, status=status.HTTP_200_OK)
    
   
""" 
    ================================
        PASSWORD RESET VIEW   
    ================================
""" 
@api_view(['POST'])
def ResetPasswordView(request):
    serializer = ResetPasswordSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        new_password = serializer.validated_data.get('new_password')
        
        if not OtpManagement.is_password_reset_verified(email):
            return Response({"response":"OTP not verified yet"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
        except User.DoesNotExist:
            return Response({"response":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        cache.delete(f"{email}_password_reset_verified")
        
        return Response({"response":"Password reset successfull"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
