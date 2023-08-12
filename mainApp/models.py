from django.db import models
from accounts.models import UserProfile
# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    created_by_name = models.CharField(max_length=150)

class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    sender_name = models.CharField(max_length=150)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    send_at = models.DateTimeField(auto_now_add=True)

