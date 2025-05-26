import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from user.models import User
from trains.models import Train
from trains.serializers import TrainSerializer
from user.decorators import jwt_required, admin_required

# Create your views here.

@csrf_exempt
@require_http_methods(["POST"])
@jwt_required
@admin_required
def add_train(request):
    try:
        # Parse JSON data
        data = json.loads(request.body)
        
        name = data.get('name')
        source = data.get('source')
        destination = data.get('destination')
        totalSeats = data.get('totalSeats')
        adminId = request.user.id

        if not all([name, source, destination, totalSeats]):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        admin = User.objects.filter(id=adminId).first()
        if not admin:
            return JsonResponse({'error': 'Admin does not exist'}, status=401)
        
        train = Train.objects.create(
            name=name,
            source=source,
            destination=destination,
            totalSeats=totalSeats,
            availableSeats=totalSeats,
            adminId=admin
        )

        train.save()
        serializer = TrainSerializer(train)

        return JsonResponse({
            'message': 'Train created successfully',
            'train': serializer.data
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
@jwt_required
@admin_required
def update_train(request, trainId):
    try:
        # Parse JSON data
        data = json.loads(request.body)
        name = data.get('name')
        source = data.get('source')
        destination = data.get('destination')
        totalSeats = data.get('totalSeats')
        admin = request.user

        if not all([name, source, destination, totalSeats]):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        # Check if train exists
        try:
            train = Train.objects.get(id=trainId)
        except Train.DoesNotExist:
            return JsonResponse({'error': 'Train not found'}, status=404)
        
        # Update train fields
        train.name = name
        train.source = source
        train.destination = destination
        train.totalSeats = totalSeats
        train.availableSeats = totalSeats  # Reset available seats
        train.adminId = admin
        train.save()

        serializer = TrainSerializer(train)

        return JsonResponse({
            'message': 'Train updated successfully',
            'train': serializer.data
        }, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
