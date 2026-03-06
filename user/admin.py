from django.contrib import admin
from .models import(
    User,
    UserProfile,
    Company, 
    WorkedCompanies
)
# Register your models here.

# ===================== User =========================
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username', 'type', 'is_active', 'created_at']
admin.site.register(User, UserAdmin)

# ===================== Employe profile =========================
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'image', 'phone', 'address', 'portfolio', 'resume', 'certificate', 'extra_field']
admin.site.register(UserProfile, UserProfileAdmin)

# ===================== Company =========================
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','slug', 'logo', 'website', 'industry', 'description', 'location', 'created_at']
admin.site.register(Company, CompanyAdmin)

# # ===================== Recuiter =========================
# class RecuiterAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'role', 'created_at']
# admin.site.register(Recuiter, RecuiterAdmin)

class WorkedCompaniesAdmin(admin.ModelAdmin):
    list_display = ['id', 'company', 'joined_at', 'resigned_at']
admin.site.register(WorkedCompanies, WorkedCompaniesAdmin)

# # ===================== Recuiter profile =========================
# class RecuiterProfileAdmin(admin.ModelAdmin):
#     list_display = ['id', 'recuiter', 'photo', 'summary']
# admin.site.register(RecuiterProfile, RecuiterProfileAdmin)