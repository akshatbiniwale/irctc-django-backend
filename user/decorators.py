import jwt
from django.conf import settings
from django.http import JsonResponse
from functools import wraps
from .models import User
import logging

logger = logging.getLogger(__name__)

def jwt_required(view_func):
    """Decorator to verify JWT token"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({
                'error': 'Authorization header missing or invalid format'
            }, status=401)
        
        try:
            token = auth_header.split(' ')[1]
            
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=['HS256']
            )
            
            user_id = payload.get('user_id')
            user = User.objects.get(id=user_id)
            
            # Add user to request
            request.user = user
            request.user_id = user_id
            
            return view_func(request, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=401)
        except Exception as e:
            logger.error(f"JWT Authentication error: {e}")
            return JsonResponse({'error': 'Authentication failed'}, status=401)
    
    return wrapper

def admin_required(view_func):
    """Decorator to verify admin role (must be used with jwt_required)"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = getattr(request, 'user', None)
        
        if not user:
            return JsonResponse({
                'error': 'User not authenticated'
            }, status=401)
        
        if user.role != 'admin':
            return JsonResponse({
                'error': 'Admin access required'
            }, status=403)
        
        return view_func(request, *args, **kwargs)
    
    return wrapper 