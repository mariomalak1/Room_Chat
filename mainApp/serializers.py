from rest_framework import serializers

from accounts.serializers import UserSerializer
from accounts.models import UserProfile
from .models import Room, Message

# your serializers here

class RoomSerializer(serializers.ModelSerializer):
    user_created_by = serializers.SerializerMethodField()

    def get_user_created_by(self, ob):
        return UserSerializer(ob.created_by).data

    class Meta:
        model = Room
        fields = ["name", "user_created_by", "id"]

class MessagesSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    class Meta:
        model = Message
        fields = ["sender", "send_at", "id", "room", "content"]


class NormalMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["sender", "send_at", "id", "room", "content"]
