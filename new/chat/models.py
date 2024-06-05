from django.db import models
from myaccount.models import Account

# Create your models here.


class Conversation(models.Model):
    user1 = models.ForeignKey(Account, related_name='conversations_as_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(Account, related_name='conversations_as_user2', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user1', 'user2')
        ordering = ['-time']

    def __str__(self):
        return f"Conversation between {self.user1.username} and {self.user2.username}"

class PrivateMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    message = models.CharField(max_length=50)
    issuer = models.ForeignKey(Account, related_name='messages_issuer', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Account, related_name='messages_receiver', on_delete=models.CASCADE)
    moment = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-moment']

    def __str__(self):
        
        return f"{self.issuer} send message"
    

    

class UserBlocked(models.Model):
    user_who_block = models.ForeignKey(Account, related_name='blocking', on_delete=models.CASCADE)
    user_blocked = models.ForeignKey(Account, related_name='blocked', on_delete=models.CASCADE)


    class Meta:
        unique_together = ('user_who_block', 'user_blocked')

    def __str__(self) :
        return f'you blocked {self.user_blocked}'
    
