from django.db import models
from django.http import HttpResponse

from account.models import Account

# Create your models here.

class Friends(models.Model):
    user1 = models.ForeignKey(Account, related_name='friendships', on_delete=models.CASCADE)
    friends = models.ManyToManyField(Account, related_name='friends', blank=True)
    relation_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user1.username

    def add_friend(self, account):
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()
        
    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)
            self.save()



