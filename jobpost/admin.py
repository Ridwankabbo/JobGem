from django.contrib import admin
from .models import JobPost, Applications
# Register your models here.

class JobPostAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'company', 'title', 'description', 'requirements', 'location', 'vacancy', 'experience', 'posted_at', 'dedline']
    
admin.site.register(JobPost, JobPostAdmin)

class ApplicationsPosts(admin.ModelAdmin):
    
    list_display = ['id', 'seeker', 'job', 'status', 'applied_at' ]
    
admin.site.register(Applications, ApplicationsPosts)
