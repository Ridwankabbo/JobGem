from rest_framework import serializers
from .models import (
    User,
    EmployeProfile,
    Recuiter, 
    RecuiterProfile,
    Company
)
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
        user = User.objects.create_user(
            email = validated_data.get('email'),
            username  = validated_data.get('username'),
            password = validated_data.get('password'),
            type = validated_data.get('type')
        )
        
        return user

""" 
    ==================================
        OTP VERIFICATION SERIALIZER 
    ==================================
"""  
class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    purpose = serializers.CharField()
    

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
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()
    
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email isn't exist")
        return value
    
    def validate(self, data):
        if not data['new_password'] == data['confirm_password']:
            raise serializers.ValidationError("new password and confirm password doesn't match")
        return data
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
    
""" 
    ==================================
        USER PROFILE SERIALIZER
    ==================================
"""
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
        ]
        
""" 
    ==================================
        EMPLOYE PROFILE SERIALIZER
    ==================================
"""
class EmployeProfileSerializer(serializers.ModelSerializer):
    employe = UserProfileSerializer()
    class Meta:
        model = EmployeProfile
        fields=['employe', 'image', 'phone', 'address', 'portfolio','resume', 'certificate']
        
""" 
    ==================================
        RECUITER SERIALIZER
    ==================================
"""
class RecuiterSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Recuiter
        fields = ['id', 'user', 'company', 'role']
        
""" 
    ==================================
        RECUITER PROFILE SERIALIZER
    ==================================
"""
class RecuiterProfileSerializer(serializers.ModelSerializer):
    retuiter = RecuiterProfile()
    class Meta:
        model = RecuiterProfile
        fields = ['recuiter', 'photo', 'summary', 'social_links']
        
""" 
    ==================================
        COMPANY PROFILE SERIALIZER
    ==================================
"""
class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'slug', 'website', 'industry', 'discription', 'location']
        
        

  
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
        elif email and not password:
            raise exceptions.AuthenticationFailed("Must inculde password")
        elif password and not email:
            raise exceptions.AuthenticationFailed("Must include email")
        else:
            raise exceptions.AuthenticationFailed("Must include email and password")
        return super().validate(attrs)