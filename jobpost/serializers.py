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
        fields = ['id', 'title', 'company', 'location', 'experience', 'status', 'dedline']
        
""" 
    ==============================
        JOB POST DETAILS SERIALIZER
    ==============================
"""
class JobPostDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = ['id', 'title', 'company', 'description', 'requirements', 'location', 'vacancy', 'experience', 'status', 'dedline', 'posted_at']

""" 
    ==============================
        JOB APPLICATION SERIALIZER
    ==============================
"""
class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applications
        fields = ['id','seeker', 'job', 'status', 'applied_at']
        read_only_fields = ['seeker']
        
    def validate(self, data):
        if Applications.objects.filter(seeker=self.context['request'].user, job=data['job']).exists():
            raise serializers.ValidationError("This user already applied for this job")
        return data

        
    def create(self, validated_data):
        seeker = self.context['request'].user
        
        try:
            application = Applications.objects.create(
                seeker = seeker,
                job = validated_data.get('job'),
            )
        except AttributeError:
            raise ValueError({
                "response":"user not found"
            })
            
        return application
