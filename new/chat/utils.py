from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication
from myaccount.models import Account

@database_sync_to_async
def get_user(validated_token):
    try:
        user_id = validated_token[JWTAuthentication.user_id_field]
        user = Account.objects.get(**{JWTAuthentication.user_id_field: user_id})
        return user
    except Account.DoesNotExist:
        return AnonymousUser()

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            try:
                auth_header = headers[b'authorization'].decode().split()
                if auth_header[0].lower() == 'bearer':
                    token = auth_header[1]
                    UntypedToken(token)
                    validated_token = JWTAuthentication().get_validated_token(token)
                    scope['user'] = await get_user(validated_token)
            except (InvalidToken, TokenError):
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        return await self.inner(scope, receive, send)