import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from user.models import User
from django.db import IntegrityError
from user.utils import generate_jwt_token

# Create your views here.

@csrf_exempt
@require_http_methods(["POST"])
def register_user(request):
    try:
        # Parse JSON data
        data = json.loads(request.body)
        
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        if not email or not password or not role:
            return JsonResponse({'error': 'All fields are required'}, status=400)

        user = User.objects.create(email=email, role=role)
        user.set_password(password)
        user.save()

        return JsonResponse({
            'message': 'User created successfully',
            'user': user.id
        }, status=201)
    
    except IntegrityError:
        return JsonResponse({'error': 'A user with this email already exists'}, status=400)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    try:
        # Parse JSON data
        data = json.loads(request.body)
        
        email = data.get('email')
        password = data.get('password')
    
        if not email or not password:
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        user = User.objects.filter(email=email).first()
        if not user:
            return JsonResponse({'error': 'Invalid email'}, status=401)
        
        if not user.check_password(password):
            return JsonResponse({'error': 'Invalid password'}, status=401)

        token = generate_jwt_token(user)

        return JsonResponse({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role
            }
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
