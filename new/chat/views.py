from django.shortcuts import render, get_object_or_404, redirect
from .models import PrivateMessage, UserBlocked, Conversation
from myaccount.models import Account
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
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
    if current_user not in [conversation.user1, conversation.user2]:
        return HttpResponseForbidden("You don't have access to this conversation.")
    messages = PrivateMessage.objects.filter(conversation=conversation).order_by('moment')
    response = {
        'id': conversation.id,
        'uid': conversation.user1.id if current_user == conversation.user2 else conversation.user2.id,
        'messages': [{'message': message.message, 'issuer': message.issuer.id} for message in messages],
    }
    return JsonResponse(response)