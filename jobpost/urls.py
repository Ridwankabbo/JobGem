from django.urls import path
from .views import (
    JobPostView,
    HiringPostView,
)
urlpatterns = [
    path('', JobPostView.as_view(), name='jobs'),
    path('post/hiring/', HiringPostView.as_view(), name='hiring-post'),
    
    
]
