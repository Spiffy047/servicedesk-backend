from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from app.services.cloudinary_service import CloudinaryService
from tickets.models import Message
from django.utils import timezone

@api_view(['POST', 'OPTIONS'])
@permission_classes([AllowAny])
@csrf_exempt
def upload_file(request):
    if request.method == 'OPTIONS':
        from django.http import HttpResponse
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    
    try:
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        ticket_id = request.data.get('ticket_id')
        user_id = request.data.get('user_id', 1)
        
        if not ticket_id:
            return Response({'error': 'ticket_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        cloudinary_service = CloudinaryService()
        result = cloudinary_service.upload_image(file, ticket_id, user_id)
        
        if 'error' in result:
            return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            Message.objects.create(
                ticket_id=ticket_id,
                sender_id=user_id,
                message=f"File uploaded: {file.name}",
                message_type='file_upload',
                file_url=result['url'],
                created_at=timezone.now()
            )
        except Exception as e:
            print(f"Failed to create timeline message: {e}")
        
        return Response({
            'success': True,
            'url': result['url'],
            'public_id': result['public_id'],
            'file_name': file.name,
            'file_size': result.get('bytes', 0)
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST', 'OPTIONS'])
@permission_classes([AllowAny])
@csrf_exempt
def upload_image(request):
    if request.method == 'OPTIONS':
        from django.http import HttpResponse
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    
    try:
        file = request.FILES.get('file') or request.FILES.get('image')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        ticket_id = request.data.get('ticket_id', 'temp')
        user_id = request.data.get('user_id', 1)
        
        cloudinary_service = CloudinaryService()
        result = cloudinary_service.upload_image(file, ticket_id, user_id)
        
        if 'error' in result:
            return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'success': True,
            'url': result['url'],
            'secure_url': result['url'],
            'public_id': result['public_id'],
            'width': result.get('width', 0),
            'height': result.get('height', 0),
            'format': result.get('format', 'unknown'),
            'bytes': result.get('bytes', 0)
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)