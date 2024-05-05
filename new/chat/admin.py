from django.contrib import admin
from .models import Conversation, UserBlocked, PrivateMessage

admin.site.register(Conversation)
admin.site.register(PrivateMessage)
admin.site.register(UserBlocked)

