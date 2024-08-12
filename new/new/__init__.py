import os
import django
from django.conf import settings
from django.db import connection
import time
from django.core.management.base import BaseCommand
django.setup()

from myaccount.models import Account

class Command(BaseCommand):
    help = 'Updates is_connected and is_in_game status for all accounts'

    def handle(self, *args, **kwargs):
        self.wait_for_db()
        accounts = Account.objects.all()
        accounts.update(is_connected=False)
        accounts.update(is_in_game=False)
        self.stdout.write(self.style.SUCCESS('Successfully updated account status'))
    
    def wait_for_db(self):
        while True:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    break
            except Exception as e:
                print(f"Database not ready: {e}")
                time.sleep(1)