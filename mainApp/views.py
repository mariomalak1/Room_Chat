from django.shortcuts import get_object_or_404
from django.core import paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.views import CustomAuthentication
from .models import Room, Message
from .serializers import RoomSerializer, MessagesSerializer
# Create your views here.

class RoomView(APIView):

    # get all rooms
    def get(self, request):
        query_search = request.GET.get("name", "")
        page = request.GET.get("page", 1)
        per_page = 10

        rooms = Room.objects.filter(name__icontains=query_search).all()
        room_paginator = paginator.Paginator(rooms, per_page=per_page)

        if int(page) > room_paginator.num_pages:
            page = room_paginator.num_pages
        elif int(page) < 1:
            page = 1

        serializer = RoomSerializer(room_paginator.page(page), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # create new room
    def post(self, request):
        token = CustomAuthentication.get_token_or_none(request)
        if not token:
            return Response({"error":"you must be authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        user_ = token.user
        data = request.data.copy()
        data["created_by"] = user_.id
        serializer = RoomSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageView(APIView):
    def get(self, request):
        room_id = request.GET.get("room_id")
        room = get_object_or_404(Room, id=room_id)
        messages = Message.objects.filter(room=room).all()
        serializer = MessagesSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        token = CustomAuthentication.get_token_or_none(request)
        if not token:
            return Response({"error":"you must be authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        room_id = request.GET.get("room_id")
        room = get_object_or_404(Room, id=room_id)

        data = request.data.copy()
        data["room"] = room.id
        data["sender"] = token.user.id

        serializer = MessagesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"Done":"ok"})



