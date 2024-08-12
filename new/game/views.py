from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import partie
from myaccount.models import Account
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from django.db.models import Prefetch, Q
from .serializers import GameSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from .consumers import PongConsumer
from .globals import setPlayer, getPlayer, removePlayer, setGame, getGame, removeGame, setCups, getCup, removeCup, queue, nb_room, players, games, cups, matchmaking_task
import asyncio
from .pongGame import pongGame, matchmaking
from .tournament import tournament
from myaccount.models import Account
from .player import Player
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync

class UserHistory(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        userhistory = get_object_or_404(Account, id=user_id)
        try:
            history = partie.objects.filter(Q(player1=userhistory) | Q(player2=userhistory)).order_by('-time') #[:10]
            paginator = PageNumberPagination()
            paginator.page_size = 10
            history_page = paginator.paginate_queryset(history, request)
            serializer = GameSerializer(history_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=404)

class UserStatus(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("UserStatus")
        user = request.user
        player = getPlayer(user.id)
        return JsonResponse({
            'type': 'status',
            'in_lobby': player.in_lobby,
            'in_cup': player.in_cup,
            'matches' : player.cup.all_rounds if player.in_cup != False else None,
            'in_queue': player.in_queue,
            'in_queue_cup': player.in_queue_cup,
        }, status=200)

class GameInfo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        player = getPlayer(user.id)
        if player.room:
            return JsonResponse({
                'type': 'game_info',
                'left': player.room.left_player.id if player.room.left_player else None,
                'right': player.room.right_player.id if player.room.right_player else None,
                'left_username': player.room.left_player.name if player.room.left_player else None,
                'right_username': player.room.right_player.name if player.room.right_player else None,
            }, status=200)
        return JsonResponse({'message': 'not in game'}, status=200)
    
class JoinQueue(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        player = getPlayer(user.id)
        async_to_sync(player.join_queue)()
        return JsonResponse({'message': 'Joined the queue'}, status=200)
    
class LeaveQueue(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        player = getPlayer(user.id)
        async_to_sync(player.leave_queue)()
        return JsonResponse({'message': 'Left the queue'}, status=200)
    
class MovePad(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        player = getPlayer(user.id)
        direction = request.query_params.get('direction')
        try:
            direction = int(direction)
        except:
            return JsonResponse({'error': 'Invalid direction'}, status=400)
        if direction < -1 or direction > 1:
            return JsonResponse({'error': 'Invalid direction'}, status=400)
        player.move(direction)
        return JsonResponse({'message': 'Pad moved'}, status=200)

class CreateAi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        player = getPlayer(user.id)
        diff = request.query_params.get('diff')
        print(diff)
        try:
            diff = int(diff)
        except:
            return JsonResponse({'error': 'Invalid difficulty'}, status=400)
        if diff < 1 or diff > 4:
            return JsonResponse({'error': 'Invalid difficulty'}, status=400)
        async_to_sync(player.setup_ai_game)(diff)
        return JsonResponse({'message': 'AI created'}, status=200)
    
class JoinCup(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        player = getPlayer(user.id)
        async_to_sync(player.join_cup)()
        return JsonResponse({'message': 'Joined the cup'}, status=200)
    
class LeaveCup(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        player = getPlayer(user.id)
        async_to_sync(player.leave_cup)()
        return JsonResponse({'message': 'Left the cup'}, status=200)

class JoinPrivateGame(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, room_name):
        user = request.user
        player = getPlayer(user.id)
        try:
            room_name = room_name.replace(" ", "")
            player1 = int(room_name.split("-")[0])
            player2 = int(room_name.split("-")[1])
        except:
            return JsonResponse({'error': 'Invalid room name'}, status=400)
        if player1 != player.id and player2 != player.id:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        async_to_sync(player.join_private_game)(room_name)
        return JsonResponse({'message': 'Joined the room'}, status=200)

class UpdateUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        player = getPlayer(user.id)
        if (request.data['name']):
            player.name = request.data['name']
            return JsonResponse({'message': 'User updated'}, status=200)
        return JsonResponse({'error': 'Invalid name'}, status=400)
