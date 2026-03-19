from django.urls import path
from .views import (
    JobPostView,
    PostDetailsView,
    HiringPostView,
    ApplayJobApplication,
)
urlpatterns = [
    path('', JobPostView.as_view(), name='jobs'),
    path('post/<int:post_id>/', PostDetailsView, name='post-detail'),
    path('post/hiring/', HiringPostView.as_view(), name='hiring-post'),
    path('job/applay/', ApplayJobApplication.as_view(), name='applay-job-application'),
    
]
