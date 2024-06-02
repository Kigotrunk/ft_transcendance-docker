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

    def __call__(self, scope):
        return JWTAuthMiddlewareInstance(scope, self)

class JWTAuthMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.scope = scope
        self.middleware = middleware

    async def __call__(self, receive, send):
        headers = dict(self.scope['headers'])
        if b'authorization' in headers:
            try:
                auth_header = headers[b'authorization'].decode().split()
                if auth_header[0].lower() == 'bearer':
                    token = auth_header[1]
                    UntypedToken(token)
                    validated_token = JWTAuthentication().get_validated_token(token)
                    self.scope['user'] = await get_user(validated_token)
            except (InvalidToken, TokenError):
                self.scope['user'] = AnonymousUser()
        else:
            self.scope['user'] = AnonymousUser()

        inner = self.middleware.inner(self.scope)
        return await inner(receive, send)