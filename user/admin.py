from django.contrib import admin
from .models import(
    User,
    EmployeProfile,
    Recuiter,
    RecuiterProfile,
    Company
)
# Register your models here.

# ===================== User =========================
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username', 'type', 'is_active', 'created_at']
admin.site.register(User, UserAdmin)

# ===================== Employe profile =========================
class EmployeProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'employe', 'image', 'phone', 'address', 'portfolio', 'resume', 'certificate', 'extra_field']
admin.site.register(EmployeProfile, EmployeProfileAdmin)

# ===================== Company =========================
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'logo', 'website', 'industry', 'description', 'location', 'created_at']
admin.site.register(Company, CompanyAdmin)

# ===================== Recuiter =========================
class RecuiterAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'company', 'role', 'created_at']
admin.site.register(Recuiter, RecuiterAdmin)

# ===================== Recuiter profile =========================
class RecuiterProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'recuiter', 'photo', 'summary']
admin.site.register(RecuiterProfile, RecuiterProfileAdmin)