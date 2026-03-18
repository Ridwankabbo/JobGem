from django.shortcuts import render
from .models import JobPost, Applications
from django.db.models import Q
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
        querry = request.GET.get('querry')
        job_filter = Q()
        if querry is not None:
            words = querry.split()
            for word in words:
                job_filter &= (
                    Q(title__icontains=word) | 
                    Q(description__icontains=word)
                )
            jobs = JobPost.objects.filter(job_filter, status="OPEN").distinct()
            # print(jobs)
            serializer = JobPostSerializer(jobs, many=True)
            return Response(serializer.data)
        
        jobs = JobPost.objects.filter(status='OPEN').all()
        serializer = JobPostSerializer(jobs, many=True)
        return Response(serializer.data)
    

    
    # def post(self, request):
    #     query = request.data.get('query')
    #     jobs = JobPost.objects.filter(title=query, status="OPEN")
    #     serializer = JobPostSerializer(jobs, many=True)
    #     return Response(serializer.data)
    
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
        
        
    def patch(self, request):
        post = JobPost.objects.get(id=request.data.get('post_id'))
        serializer = JobPostSerializer(post, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"response":"Post updated successfully"})
        return Response({"response":f"{serializer.errors}"})
    
    
    def delete(self, request):
        post_id = request.data.get('post_id')
        JobPost.objects.get(id=post_id).delete()
        return Response({"response":"post delited"})

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
        
    def delete(self, request):
        post_id = request.data.get('post_id')
        Applications.objects.get(job=post_id).delete()
        return Response({"response":"application delited"})
            
