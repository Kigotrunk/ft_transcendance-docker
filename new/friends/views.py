from django.shortcuts import render, redirect, get_object_or_404
from friends.models import Friends
from myaccount.models import Account

# Create your views here.

def  new_friend_view(request, user_id):

    if not request.user.is_authenticated:
        return redirect('login')
    
    new_friend_user = get_object_or_404(Account, id=user_id)
    key_friend, not_existing = Friends.objects.get_or_create(user1=request.user)
    if key_friend.friends.filter(id=new_friend_user.id):
        return redirect('profil', user_id=new_friend_user.id)
    else:
        key_friend.friends.add(new_friend_user)
        key_friend.save()
        return redirect('profil', user_id=new_friend_user.id)


