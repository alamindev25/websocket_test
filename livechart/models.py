from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# livechart/models.py
from django.db import models

class ChartData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=150, null=True, blank=True)  # Alternative to user field
    value = models.FloatField(null=True, blank=True)  # Make value optional
    message = models.TextField(null=True, blank=True)  # Add message field
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        user_display = self.username or (self.user.username if self.user else 'Anonymous')
        content = self.message if self.message else f"Value: {self.value}"
        return f"{user_display}: {content} at {self.created_at}"
