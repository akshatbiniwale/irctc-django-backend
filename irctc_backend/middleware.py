import jwt
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from user.models import User
import logging

logger = logging.getLogger(__name__)

class VerifyToken(MiddlewareMixin):
    def process_request(self, request):
        exempt_paths = [
            '/api/auth/register/',
            '/api/auth/login/',
        ]
        
        if any(request.path.startswith(path) for path in exempt_paths):
            return None
            
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
            
            request.user = user
            request.user_id = user_id
            
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=401)
        except Exception as e:
            logger.error(f"JWT Authentication error: {e}")
            return JsonResponse({'error': 'Authentication failed'}, status=401)
        
        return None

class IsAdmin(MiddlewareMixin):
    def process_request(self, request):
        admin_only_paths = [
            '/api/trains/add/',
            '/api/trains/update/',
            '/api/trains/delete/',
        ]
        
        if any(request.path.startswith(path) for path in admin_only_paths):
            user = getattr(request, 'user', None)
            
            if not user:
                return JsonResponse({
                    'error': 'User not authenticated'
                }, status=401)
            
            if user.role != 'admin':
                return JsonResponse({
                    'error': 'Admin access required'
                }, status=403)
        
        return None