# path: a_rtchat/auth_middleware.py
import urllib.parse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async

User = get_user_model()
jwt_auth = JWTAuthentication()

@database_sync_to_async
def get_user_from_token(token):
    """
    Usa Simple JWT para validar token e retornar User (ou AnonymousUser on fail).
    """
    if not token:
        return None
    try:
        validated = jwt_auth.get_validated_token(token)
        user = jwt_auth.get_user(validated)
        return user
    except Exception:
        return None

class TokenAuthMiddleware(BaseMiddleware):
    """
    Extrai token do querystring (?token=...) e configura scope['user'].
    Uso: TokenAuthMiddleware(inner) -> then AuthMiddlewareStack/timeouts
    """
    async def __call__(self, scope, receive, send):
        # parse query_string
        query_string = scope.get("query_string", b"").decode()
        qs = urllib.parse.parse_qs(query_string)
        token_list = qs.get("token") or qs.get("access_token")
        token = token_list[0] if token_list else None

        user = await get_user_from_token(token)
        scope["user"] = user or None

        return await super().__call__(scope, receive, send)
