"""
URL configuration for new project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from front import views
from django.conf.urls import include
from django.urls import include

urlpatterns = [
    path('accounts/', include('allauth.urls')),
]


from myaccount.views import (
    register_view,
    login_view,
    logout_view,
    update_user_view,
)

from friends.views import (
    new_friend_view,
)

from chat.views import (
    chat_view,
    #all_conversations_view,
)

from game.views import (
    pong
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profil/', include('myaccount.urls', namespace = 'account')),
    path('update/', update_user_view, name='update_user'),
    path('profile/', views.profile , name='profile'),
    path('chat/', chat_view, name='chat_view'),
    #path('chat/<str:username1>/<str:username2>', chat_view, name='chat_view'),
    #path('chat/', all_conversations_view, name='all_conversations'),
    path('add-friend/<int:user_id>/', new_friend_view, name='add_friend'),
    path('accounts/', include('allauth.urls')),
    path('game/', pong, name='game'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
