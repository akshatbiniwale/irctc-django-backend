import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User
from django.db import IntegrityError
from user.utils import generate_jwt_token

# Create your views here.

class RegisterUser(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            role = request.data.get('role')

            if not email or not password or not role:
                return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create(email=email, role=role)
            user.set_password(password)
            user.save()

            return Response({
                'message': 'User created successfully',
                'user': user.id
            }, status=status.HTTP_201_CREATED)
        
        except IntegrityError:
            return Response({'error': 'A user with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginUser(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
        
            if not email or not password:
                return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.filter(email=email).first()
            if not user:
                return Response({'error': 'Invalid email'}, status=status.HTTP_401_UNAUTHORIZED)
            
            if not user.check_password(password):
                return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

            token = generate_jwt_token(user)

            return Response({
                'message': 'Login successful',
                'token': token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'role': user.role
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
