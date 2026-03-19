from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_history')
    message = models.TextField()
    response = models.TextField()
    responsed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.message}"
    
    class Meta:
        ordering = ['responsed_at']
