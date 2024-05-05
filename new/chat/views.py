from django.shortcuts import render, get_object_or_404, redirect
from .models import PrivateMessage, UserBlocked, Conversation
from account.models import Account
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import FormMessage
from django.urls import reverse
from django.db.models import Prefetch
# Create your views here.

@login_required
def chat_view(request, username1, username2):
    user1 = get_object_or_404(Account, username=username1)
    user2 = get_object_or_404(Account, username=username2)
    conversation = Conversation.objects.filter(user1=user1, user2=user2).union(Conversation.objects.filter(user1=user2, user2=user1)).first()
    if not conversation:
        conversation = Conversation(user1=user1, user2=user2)
        conversation.save()
    form = FormMessage(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            private_message = form.save(commit=False)
            private_message.issuer = request.user
            private_message.receiver = user1 if private_message.issuer == user2 else user2
            private_message.conversation = conversation
            private_message.save()
        return redirect('chat_view', username1=username1, username2=username2)
    else:
        form = FormMessage()
    messages = PrivateMessage.objects.filter(conversation=conversation).order_by('moment')
    context = {
        'conversation' : conversation,
        'messages' : messages,
        'form' : form,
        'user1' : user1,
        'user2' : user2,
    }
    return render(request, 'chat/chat.html', context)


@login_required
def all_conversations_view(request):
    current_user = request.user
    conversations = Conversation.objects.filter(user1=current_user) | Conversation.objects.filter(user2=current_user)
    context = {
        'conversations': conversations,
    }
    return render(request, 'chat/all_conversations.html', context)
            
    




# @login_required
# def send_message_view(request, user2_id=None):
#     if request.method == 'POST':
#         sender = request.user
#         recipient_id = user2_id if user2_id else request.POST.get('recipient_id')
#         if recipient_id is None:
#             return JsonResponse({'error': 'Recipient ID not provided.'}, status=400)
#         try:
#             recipient = Account.objects.get(id=recipient_id)
#         except ObjectDoesNotExist:
#             return JsonResponse({'error': 'Recipient not found.'}, status=404)
#         if UserBlocked.objects.filter(user_who_block=recipient, user_blocked=sender).exists():
#             return JsonResponse({'error': 'Recipient has blocked you.'}, status=403)
#         content = request.POST.get('content')
#         if not content:
#             return JsonResponse({'error': 'Content is required.'}, status=400)
#         message = PrivateMessage(issuer=sender, receiver=recipient, message=content)
#         message.save()
#         return JsonResponse({'success': 'Message sent successfully.'}, status=200)



# @login_required
# def receive_messages(request):
#     user = request.user
#     senders = PrivateMessage.objects.filter(receiver=user).values_list('issuer', flat=True).distinct()
#     senders_with_messages = Account.objects.filter(id__in=senders).prefetch_related(Prefetch('sent_private_messages', queryset=PrivateMessage.objects.filter(receiver=user).order_by('-moment'),
#             to_attr='messages_to_user'
#         )
#     )
#     blocked_users = UserBlocked.objects.filter(user_who_block=user).values_list('user_blocked', flat=True)
#     senders_with_messages = senders_with_messages.exclude(id__in=blocked_users)
#     response_data = []
#     for sender in senders_with_messages:
#         messages_list = []
#         for message in sender.messages_to_user:
#             messages_list.append({
#                 'id': message.id,
#                 'content': message.message,
#                 'timestamp': message.moment.strftime('%Y-%m-%d %H:%M:%S'),
#             })
#         response_data.append({
#             'sender': sender.username,
#             'messages': messages_list,
#         })
#     return JsonResponse({'messages': response_data})

