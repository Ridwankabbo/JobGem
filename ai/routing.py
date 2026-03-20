from django.urls import re_path
from .consumers import AiAgentConsummer

websocket_urlpatterns = [
    re_path(r'ws/jobgem-ai/$', AiAgentConsummer.as_asgi()),
]