from django.db import models
from accounts.models import UserProfile
# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    created_by_name = models.CharField(max_length=150)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.created_by_name = self.created_by.username
        super(Room, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def __str__(self):
        return self.name + " - " + str(self.created_by)

class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=False)
    sender_name = models.CharField(max_length=150)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    send_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=False, blank=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.sender_name = self.sender.username
        super(Message, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
