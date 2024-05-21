from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.rooms, name='rooms'),
    path('game/<str:room_name>/', views.game, name='game'),
]
