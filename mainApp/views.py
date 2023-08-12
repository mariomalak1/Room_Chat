from django.core import paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Room
from .serializers import RoomSerializer
# Create your views here.

class RoomView(APIView):
    # get all rooms
    def get(self, request):
        query_search = request.GET.data.get("name", "")
        page = request.GET.data.get("page", 1)
        per_page = 10

        rooms = Room.objects.filter(name__icontains=query_search).all()
        room_paginator = paginator.Paginator(rooms, per_page=per_page)

        if int(page) > paginator.num_pages:
            page = paginator.num_pages
        elif int(page) < 1:
            page = 1

        serializer = RoomSerializer(room_paginator.page(page), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # create new room
    def post(self, request):
        data = request.data
        serializer = RoomSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
