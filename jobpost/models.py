from django.db import models
from user.models import Company, User
# Create your models here.


""" 
    ========================
        JOB POST MODEL
    ========================
"""
class JobPost(models.Model):
    class Job_status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        CLOSE = 'CLOSE', 'Close'
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField()
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=255)
    vacancy = models.IntegerField()
    experience = models.CharField()
    status = models.CharField(choices=Job_status.choices, default=Job_status.OPEN)
    dedline = models.DateField(null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)

""" 
    ========================
        JOB POST MODEL
    ========================
"""
class Applications(models.Model):
    class application_status(models.TextChoices):
        APPLIED = 'APPLIED', 'Applied'
        REVIEWED = 'REVIEWED', 'Reviewed'
        CANCLED = 'CANCLED', 'Cancled'
    seeker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applied_applications')
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='job_applications')
    status = models.CharField(choices=application_status.choices, default=application_status.APPLIED)
    applied_at = models.DateTimeField(auto_now_add=True)
    
