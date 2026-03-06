from django.shortcuts import render
from .models import JobPost, Applications
from .serializers import JobApplicationSerializer, JobPostSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import (
    IsCompanyRecuiter,
)
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework import status
# Create your views here.


""" 
    ========================
        VIEW JOBS POST
    ========================
"""
class JobPostView(APIView):
    
    def get(self, request):
        jobs = JobPost.objects.all()
        serializer = JobPostSerializer(jobs, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        query = request.data.get('query')
        jobs = JobPost.objects.filter(title=query, status="OPEN")
        serializer = JobPostSerializer(jobs, many=True)
        return Response(serializer.data)
    
""" 
    ========================
        HIRING VIEW
    ========================
"""
class HiringPostView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = JobPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "response":"Post successfull"
            }, status=status.HTTP_200_OK)
        return Response({
            "response":f"{serializer.errors}"
        }, status=status.HTTP_400_BAD_REQUEST)

""" 
    ===========================
        JOB APPLICATION VIEW
    ===========================
"""    
class ApplayJobApplication(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        applications = Applications.objects.filter(seeker=request.user)
        serialzer = JobApplicationSerializer(applications,  many=True)
        return Response(serialzer.data)
    
    def post(self, request):
        serializer = JobApplicationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "response":"Successfuly Applied"
            }, status=status.HTTP_200_OK)
        return Response({
            'response':f"{serializer.errors}"
        }, status=status.HTTP_400_BAD_REQUEST)
            
