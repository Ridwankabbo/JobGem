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
            user = User.objects.creat_user(
                email = validated_data.get('email'),
                username  = validated_data.get('username'),
                password = validated_data.get('password'),
                type = validated_data.get('type')
            )
            otp = GenerateOTP()
            user.opt = otp
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