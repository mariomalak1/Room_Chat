from django.urls import path
from .views import RoomView, MessageView

urlpatterns = [
    path("room", RoomView.as_view()),
    path("message", MessageView.as_view()),
]