import jwt
from django.conf import settings
from datetime import datetime, timedelta, timezone

def generate_jwt_token(user):
    """Generate JWT access token for user"""
    payload = {
        'user_id': user.id,
        'email': user.email,
        'role': user.role,
        'exp': datetime.now(timezone.utc) + timedelta(days=7),
        'iat': datetime.now(timezone.utc),
        'iss': 'irctc_backend'
    }
    
    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm='HS256'
    )
    
    return token