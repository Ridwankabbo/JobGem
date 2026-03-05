from rest_framework import serializers
from .models import JobPost, Applications


""" 
    ==============================
        JOB POST SERIALIZER
    ==============================
"""
class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = ['id', 'title', 'company', 'description', 'requirements', 'location', 'vacancy', 'experience', 'status', 'dedline']
        

""" 
    ==============================
        JOB APPLICATION SERIALIZER
    ==============================
"""
class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applications
        fields = '__all__'
