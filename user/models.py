from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# Create your models here.

class CustomUserModel(BaseUserManager):
    
    def creat_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("Email must require")
        
        email = self.normalize_email(email)
        user = self.model(email = email, username = username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def creat_superuser(self, email, username, password=None, **extre_fields):
        user = self.creat_user(email, username, password)
        user.is_active=True
        user.is_staff=True
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        
        return user
    
    
class User(AbstractBaseUser, PermissionsMixin):
    class user_type(models.TextChoices):
        EMPLOYE = 'EMPLOYE', 'Employe'
        RECUITER = 'RECUITER', 'Recuiter'
        
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    type = models.CharField(choices=user_type.choices, default=user_type.EMPLOYE)
    otp = models.CharField(max_length=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserModel()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"name:{self.username} email:{self.email}"
    
class EmployePortfolio(models.Model):
    employe = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employe_portfolio')
    portfolio_link = models.URLField(max_length=255, null=True, blank=True) 
    
class EmployeResume(models.Model):
    employe = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employe_resume')
    resume = models.FileField()
    
class EmployeCertificates(models.Model):
    employe = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employe_certificate')
    cerficate_name = models.CharField(max_length=255)
    certificate_link = models.URLField(null=True, blank=True)
    
class EmployeExtreFields(models.Model):
    employe = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employe_extra_field')
    fild_name = models.CharField(max_length=255)
    fild_value = models.CharField(max_length=255)
    link = models.URLField(null=True, blank=True)

class EmployeProfile(models.Model):
    employe = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employe_profile')
    image = models.ImageField(upload_to='user_profile_image', null=True, blank=True)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=255)
    portfolio = models.ForeignKey(EmployePortfolio, on_delete=models.CASCADE)
    resume = models.ForeignKey(EmployeResume, on_delete=models.CASCADE)
    certificate = models.ForeignKey(EmployeCertificates, on_delete=models.CASCADE)
    extra_field = models.ForeignKey(EmployeExtreFields, on_delete=models.CASCADE)
    
    
    
    
        
        
