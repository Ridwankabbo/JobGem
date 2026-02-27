from rest_framework import serializers
from .models import User
from .utils import GenerateOTP
""" 
    ==================================
        USER REGISTRATION SERIALIZER 
    ==================================
"""
class UserRegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'type']
        
        
    def create(self, validated_data):
        
        try:
            user = User.objects.create_user(
                email = validated_data.get('email'),
                username  = validated_data.get('username'),
                password = validated_data.get('password'),
                type = validated_data.get('type')
            )
            otp = GenerateOTP()
            print(otp)
            user.otp = otp
            user.save()
        except AttributeError:
            raise ValueError({"errro":"Otp not found"})
        
        return user

""" 
    ==================================
        OTP VERIFICATION SERIALIZER 
    ==================================
"""  
class AccountVerificationByOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    

""" 
    ==================================
        FORGOT PASSWORD SERIALIZER 
    ==================================
"""
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

""" 
    ==================================
        RESET PASSWORD SERIALIZER 
    ==================================
"""
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    password = serializers.CharField()
  
  
""" 
    =====================================
        CUSTOM TOKEN OBTAIN SERISLIZER 
    =====================================
"""  
    
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions
from django.contrib.auth import authenticate
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    username_fiels = 'email'
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)

            if not user:
                raise exceptions.AuthenticationFailed("No active account found with this user")
            if not user.is_active:
                raise exceptions.AuthenticationFailed("Account isn't active")
        elif user and not password:
            raise exceptions.AuthenticationFailed("Must inculde password")
        elif password and not user:
            raise exceptions.AuthenticationFailed("Must include email")
        else:
            raise exceptions.AuthenticationFailed("Must include email and password")
        return super().validate(attrs)