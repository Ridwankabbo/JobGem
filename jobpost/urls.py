from django.urls import path
from .views import (
    JobPostView,
    HiringPostView,
    ApplayJobApplication,
)
urlpatterns = [
    path('', JobPostView.as_view(), name='jobs'),
    path('post/hiring/', HiringPostView.as_view(), name='hiring-post'),
    path('job/applay/', ApplayJobApplication.as_view(), name='applay-job-application'),
    
]
