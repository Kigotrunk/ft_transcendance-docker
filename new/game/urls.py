from django.urls import path
from . import views

urlpatterns = [
    path('history/<int:user_id>/', views.UserHistory.as_view() , name='player_history'),
    path('status/', views.UserStatus.as_view(), name='status'),
    path('join_queue/', views.JoinQueue.as_view(), name='join_queue'),
    path('leave_queue/', views.LeaveQueue.as_view(), name='leave_queue'),
    path('move/', views.MovePad.as_view(), name='move_pad'),
    path('create_ai/', views.CreateAi.as_view(), name='create_ai'),
    path('join_cup/', views.JoinCup.as_view(), name='join_cup'),
    path('leave_cup/', views.LeaveCup.as_view(), name='leave_cup'),
    path('update_user/', views.UpdateUser.as_view(), name='update_user'),
    path('join_private_game/<str:room_name>/', views.JoinPrivateGame.as_view(), name='join_private_game'),
    path('info/', views.GameInfo.as_view(), name='game_info'),
]
