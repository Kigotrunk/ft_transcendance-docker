from django.urls import path
from . import views

urlpatterns = [
    path("", views.lobby, name="game"),
    path("<str:room_name>/", views.room, name="room"),
]