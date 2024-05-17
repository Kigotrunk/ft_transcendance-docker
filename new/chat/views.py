from django.shortcuts import render, get_object_or_404, redirect
from .models import PrivateMessage, UserBlocked, Conversation
from myaccount.models import Account
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import FormMessage
from django.urls import reverse
from django.db.models import Prefetch
# Create your views here.



@login_required
def chat_view(request):
    current_user = request.user
    conversations_with_other_user = []
    conversations = Conversation.objects.filter(user1=current_user) | Conversation.objects.filter(user2=current_user)
    for conversation in conversations:
        other_user = conversation.user1 if conversation.user2 == current_user else conversation.user2
        conversations_with_other_user.append((conversation, other_user))
    selected_conversation_id = request.GET.get('conversation_id')
    selected_conversation = None
    messages = []
    form = FormMessage()
    if selected_conversation_id:
        selected_conversation = get_object_or_404(Conversation, id=selected_conversation_id)
        messages = PrivateMessage.objects.filter(conversation=selected_conversation).order_by('moment')
        if request.method == 'POST':
            form = FormMessage(request.POST)
            if form.is_valid():
                private_message = form.save(commit=False)
                private_message.issuer = current_user
                private_message.receiver = selected_conversation.user1 if current_user == selected_conversation.user2 else selected_conversation.user2
                private_message.conversation = selected_conversation
                private_message.save()
                return redirect(f'/chat/?conversation_id={selected_conversation_id}') 
    context = {
        'conversations_with_other_user': conversations_with_other_user,
        'selected_conversation': selected_conversation,
        'messages': messages,
        'form': form,
    }

    return render(request, 'chat/chat.html', context)


# @login_required
# def chat_view(request):
#     current_user = request.user
#     conversations_with_other_user = []
#     conversations = Conversation.objects.filter(user1=current_user) | Conversation.objects.filter(user2=current_user)
#     for conversation in conversations:
#         other_user = conversation.user1 if conversation.user2 == current_user else conversation.user2
#         conversations_with_other_user.append({
#             'id': conversation.id,
#             'other_user': other_user.username,
#             'other_user_id': other_user.id
#         })

#     selected_conversation_id = request.GET.get('conversation_id')
#     selected_conversation = None
#     messages = []
#     form = FormMessage()
#     if selected_conversation_id:
#         selected_conversation = get_object_or_404(Conversation, id=selected_conversation_id)
#         messages = PrivateMessage.objects.filter(conversation=selected_conversation).order_by('moment')
#         if request.method == 'POST':
#             form = FormMessage(request.POST)
#             if form.is_valid():
#                 private_message = form.save(commit=False)
#                 private_message.issuer = current_user
#                 private_message.receiver = selected_conversation.user1 if current_user == selected_conversation.user2 else selected_conversation.user2
#                 private_message.conversation = selected_conversation
#                 private_message.save()
#                 return JsonResponse({'success': True})  # Return a success response

#     context = {
#         'conversations_with_other_user': conversations_with_other_user,
#         'selected_conversation': selected_conversation.id if selected_conversation else None,
#         'messages': messages,
#         'form': form.as_p(),  # Assuming your form is a Django form, convert it to HTML
#     }

#     return JsonResponse(context)

@login_required
def chat_list(request):
    current_user = request.user
    chat_list = []
    conversations = Conversation.objects.filter(user1=current_user) | Conversation.objects.filter(user2=current_user)
    for conversation in conversations:
        other_user = conversation.user1 if conversation.user2 == current_user else conversation.user2
        chat_list.append({
            'id': conversation.id,
            'other_user': {
                'username': other_user.username,
                'id': other_user.id,
                'pp': other_user.profile_picture.url,
            }
        })
    response = {
        'conversations': chat_list,
    }
    return JsonResponse(response)

@login_required
def get_chat(request, chat_id):
    current_user = request.user
    conversation = get_object_or_404(Conversation, id=chat_id)
    if current_user != conversation.user1 and current_user != conversation.user2:
        return HttpResponseForbidden("You don't have access to this conversation.")
    
    messages = PrivateMessage.objects.filter(conversation=conversation).order_by('moment')

    form = FormMessage()
    
    response = {
        'id': conversation.id,
        'uid': conversation.user1.id if current_user == conversation.user2 else conversation.user2.id,
        'messages': [{'message': message.message, 'issuer': message.issuer.id} for message in messages],
        'form': form.as_p(),
    }
    
    return JsonResponse(response)


# @login_required
# def chat_view(request, username1, username2):
#     user1 = get_object_or_404(Account, username=username1)
#     user2 = get_object_or_404(Account, username=username2)
#     conversation = Conversation.objects.filter(user1=user1, user2=user2).union(Conversation.objects.filter(user1=user2, user2=user1)).first()
#     if not conversation:
#         conversation = Conversation(user1=user1, user2=user2)
#         conversation.save()
#     form = FormMessage(request.POST)
#     if request.method == 'POST':
#         if form.is_valid():
#             private_message = form.save(commit=False)
#             private_message.issuer = request.user
#             private_message.receiver = user1 if private_message.issuer == user2 else user2
#             private_message.conversation = conversation
#             private_message.save()
#         return redirect('chat_view', username1=username1, username2=username2)
#     else:
#         form = FormMessage()
#     messages = PrivateMessage.objects.filter(conversation=conversation).order_by('moment')
#     context = {
#         'conversation' : conversation,
#         'messages' : messages,
#         'form' : form,
#         'user1' : user1,
#         'user2' : user2,
#     }
#     return render(request, 'chat/chat.html', context)


# @login_required
# def all_conversations_view(request):
#     current_user = request.user
#     conversations = Conversation.objects.filter(user1=current_user) | Conversation.objects.filter(user2=current_user)
#     context = {
#         'conversations': conversations,
#     }
#     return render(request, 'chat/all_conversations.html', context)
            
    




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

