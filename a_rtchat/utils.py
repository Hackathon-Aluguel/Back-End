import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generate_jwt_token(user_id, minutes_valid=60):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=minutes_valid),
        "iat": datetime.utcnow(),
        "token_type": "access"
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token

