from rest_framework import serializers
from .models import (
    User,
    UserProfile,
    Company, 
    WorkedCompanies
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
        COMPANY PROFILE SERIALIZER
    ==================================
"""
class CompaniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'slug', 'website', 'industry', 'discription', 'location']
    
""" 
    ==================================
        USER  SERIALIZER
    ==================================
"""
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
        ]
        
""" 
    ==================================
        WORKED PROFILE SERIALIZER
    ==================================
"""     
class WorkdCompaniesSerializer(serializers.ModelSerializer):
    # company = CompaniSerializer( many=True, read_only=True)
    class Meta:
        model = WorkedCompanies
        fields = ['id', 'user_profile', 'company', 'joined_at', 'resigned_at']
        
    def create(self, validate_data):
        user = self.context['request'].user
        
        try:
            work = WorkedCompanies.objects.create(
                user = user,
                company = validate_data.get('company')
            )
            
        except AttributeError:
            raise ValueError("user not found")
        
        return work
        
        
""" 
    ==================================
        EMPLOYE PROFILE SERIALIZER
    ==================================
"""
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    worked_companies = WorkdCompaniesSerializer()
    class Meta:
        model = UserProfile
        fields=['user', 'image', 'phone', 'address', 'portfolio','resume', 'certificate', 'worked_companies']
        
    def validate(self, attrs):
        profile = UserProfile.objects.filter(user = self.context['request'].user)
        if profile:
            return profile
        raise ValueError("User doesn't exist")
        
# """ 
#     ==================================
#         RECUITER SERIALIZER
#     ==================================
# """
# class RecuiterSerializer(serializers.ModelSerializer):
#     user = UserProfileSerializer()
#     class Meta:
#         model = Recuiter
#         fields = ['id', 'user', 'role']
        
# """ 
#     ==================================
#         RECUITER PROFILE SERIALIZER
#     ==================================
# """
# class RecuiterProfileSerializer(serializers.ModelSerializer):
#     recuiter = RecuiterSerializer()
#     company = WorkdCompaniesSerializer(read_only=True, many=True)
#     class Meta:
#         model = RecuiterProfile
#         fields = ['recuiter', 'photo', 'summary', 'social_links', 'company']
        
        

  
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