from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# Create your models here.


""" 
    ==========================
        CUSTOM USER MODEL 
    ==========================
"""
class CustomUserModel(BaseUserManager):
    
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("Email must require")
        
        email = self.normalize_email(email)
        user = self.model(email = email, username = username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, username, password=None, **extre_fields):
        user = self.create_user(email, username, password)
        user.is_active=True
        user.is_staff=True
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        
        return user

""" 
    ==========================
        USER MODEL 
    ==========================
"""    
class User(AbstractBaseUser, PermissionsMixin):
    class user_type(models.TextChoices):
        EMPLOYE = 'EMPLOYE', 'Employe'
        RECUITER = 'RECUITER', 'Recuiter'
        ADMIN = 'ADMIN','Admin'
        NONE = '...', '...'
        
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    type = models.CharField(choices=user_type.choices, default=user_type.NONE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserModel()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"name:{self.username} email:{self.email}"

""" ============================= UNIVERSAL MODELS (COMMON MODELS) =========================""" 
# ================= USER TYPE CHOICES ===============
class user_type(models.TextChoices):
    EMPLOYE = 'EMPLOYE', 'Employe'
    RECUITER = 'RECUITER', 'Recuiter'
    ADMIN = 'ADMIN','Admin'
    NONE = '...', '...'

# =============== SOCIAL LINKS ===================
class SocialLinks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_social_links')
    name = models.CharField(max_length=100)
    link = models.URLField()
    # added_at = models.DateTimeField(auto_now_add=True)
    
# =============== PROTFOLIO ================
class Portfolios(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employe_portfolio')
    portfolio_link = models.URLField(max_length=255, null=True, blank=True) 


# =============== RESUME ================
class Resumes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employe_resume')
    resume = models.FileField()
    # added_at = models.DateTimeField(auto_now_add=True)
    
# =============== CERTIFICATE ================
class Certificates(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employe_certificate')
    cerficate_name = models.CharField(max_length=255)
    certificate_link = models.URLField(null=True, blank=True)
    # added_at = models.DateTimeField(auto_now_add=True)
    
# =============== EXTRA FIELDS ================
class ExtreFields(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employe_extra_field')
    fild_name = models.CharField(max_length=255)
    fild_value = models.CharField(max_length=255)
    link = models.URLField(null=True, blank=True)
    # added_at = models.DateTimeField(auto_now_add=True)
    
    
""" ========================================================================================="""

""" =========================== COMPANY ======================================="""
""" 
    ============================
        COMPANY DETAILS MODEL 
    ============================
"""  
class Company(models.Model):
    class industry_type(models.TextChoices):
        IT = 'IT', 'It'
        MARKETING_AGENCY = "MARKETING AGENCY", "Marketing agency"
        SOFTWARE_DEVELOPMENT ='SOFTWARE DEVELOPMENT', 'Software development'
        GRAPHIC_DESIGNE_AGENCY = 'GRAPHIC DESIGNE AGENCY', 'Graphic designe agency'
        DEFAULT = '...', '...'
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    logo = models.ImageField(upload_to='company_logo', null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    industry = models.TextField(choices=industry_type.choices, default=industry_type.DEFAULT)
    description = models.TextField(null=True, blank=True)
    location = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{slugify(self.name)}_{self.created_at}")
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.name}"
    
""" ======================================================================="""


""" 
    ==============================
        WORKED COMPANIES MODEL 
    ==============================
"""
class WorkedCompanies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    resigned_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}"


""" =========================== EMPLOYE MODELS ==========================="""

""" 
    ==========================
        EMPLOYE PROFILE MODEL 
    ==========================
"""  
class EmployeProfile(models.Model):
    employe = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employe_profile')
    image = models.ImageField(upload_to='user_profile_image', null=True, blank=True)
    phone = models.CharField(max_length=11, null=True)
    address = models.CharField(max_length=255, null=True)
    portfolio = models.ForeignKey(Portfolios, on_delete=models.CASCADE, null=True)
    resume = models.ForeignKey(Resumes, on_delete=models.CASCADE, null=True)
    certificate = models.ForeignKey(Certificates, on_delete=models.CASCADE, null=True)
    worked = models.ForeignKey(WorkedCompanies, on_delete=models.CASCADE, null=True, blank=True, related_name='worked_companies')
    extra_field = models.ForeignKey(ExtreFields, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"{self.employe.username}"
    
    
""" ======================================================================="""



""" =========================== Recuiter models ==========================="""
""" 
    ==========================
        RECUITER MODEL 
    ==========================
"""  
class Recuiter(models.Model):
    class role_type(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin',
        RECUITER = 'RECUITER', 'Recuiter' 
        DEFAULT = '...', '...'
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recuiter')
    role = models.TextField(choices=role_type.choices, default=role_type.DEFAULT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"

""" 
    ==========================
        RECUITER PROFILE MODEL 
    ==========================
"""  
class RecuiterProfile(models.Model):
    recuiter = models.ForeignKey(Recuiter, on_delete=models.CASCADE, related_name='recuiter_profile')
    photo = models.ImageField(upload_to='recuiter_profile_photo', null=True, blank=True)
    summary = models.TextField(null=True)
    company = models.ForeignKey(WorkedCompanies, on_delete=models.CASCADE, null=True, blank=True, related_name='companies')
    social_links = models.ForeignKey(SocialLinks, on_delete=models.CASCADE, null=True, related_name='recuiter_social_links')
    
    
""" ======================================================================="""
    
        
