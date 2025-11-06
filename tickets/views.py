from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from .models import Ticket, Message
from users.models import User
from notifications.models import Alert
from rest_framework import serializers

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        extra_kwargs = {
            'priority': {'required': False},
            'category': {'required': False},
            'image_url': {'required': False, 'allow_blank': True, 'allow_null': True},
        }

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

# Add CORS headers manually
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    
    def get_queryset(self):
        try:
            queryset = Ticket.objects.all()
            created_by = self.request.query_params.get('created_by')
            if created_by:
                queryset = queryset.filter(created_by=created_by)
            return queryset.order_by('-created_at')
        except Exception as e:
            print(f"Error fetching tickets: {e}")
            import traceback
            traceback.print_exc()
            return Ticket.objects.none()
    
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            print(f"Error in ticket list view: {e}")
            import traceback
            traceback.print_exc()
            return Response({'error': 'Failed to fetch tickets', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            print(f"Received ticket data: {data}")
            
            # Validate required fields
            required_fields = ['title', 'description', 'priority', 'category', 'created_by']
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                return Response({'error': f'Missing required fields: {", ".join(missing_fields)}'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Handle image_url field - remove if invalid
            if 'image_url' in data:
                image_url = data['image_url']
                if not image_url or len(str(image_url)) > 500 or not str(image_url).startswith(('http://', 'https://')):
                    data.pop('image_url', None)
            
            # Generate ticket_id if not provided
            if 'ticket_id' not in data or not data['ticket_id']:
                last_ticket = Ticket.objects.order_by('-id').first()
                next_id = (last_ticket.id + 1) if last_ticket else 1
                data['ticket_id'] = f'TKT-{next_id:04d}'
            
            # Set default values
            if 'status' not in data:
                data['status'] = 'New'
            if 'sla_violated' not in data:
                data['sla_violated'] = False
                
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                ticket = serializer.save()
                
                # Handle file upload if present
                if 'file' in request.FILES or 'image' in request.FILES:
                    file = request.FILES.get('file') or request.FILES.get('image')
                    if file:
                        try:
                            from files.views import upload_image
                            # Create a mock request for upload
                            from django.http import HttpRequest
                            upload_request = HttpRequest()
                            upload_request.FILES = {'file': file}
                            upload_request.POST = {'ticket_id': ticket.ticket_id, 'user_id': str(data['created_by'])}
                            upload_request.method = 'POST'
                            
                            # Upload image and get URL
                            upload_response = upload_image(upload_request)
                            if upload_response.status_code == 200:
                                upload_data = upload_response.data
                                if 'url' in upload_data:
                                    ticket.image_url = upload_data['url']
                                    ticket.save()
                                    print(f"Image uploaded and saved to ticket: {upload_data['url']}")
                        except Exception as upload_error:
                            print(f"Image upload failed: {upload_error}")
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(f"Validation errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            print(f"Error creating ticket: {e}")
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        try:
            # Handle malformed ticket ID by extracting numeric part
            ticket_id = kwargs.get('pk')
            if ':' in str(ticket_id):
                try:
                    ticket_id = str(ticket_id).split(':')[0]
                    kwargs['pk'] = ticket_id
                except (ValueError, IndexError):
                    return Response({'error': f'Invalid ticket ID format: {ticket_id}'}, status=status.HTTP_400_BAD_REQUEST)
            
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            data = request.data.copy()
            
            # For PUT requests with single field, use partial update
            if request.method == 'PUT' and len(data) == 1:
                partial = True
            
            # Handle assignment
            if 'assigned_to' in data:
                old_assigned_to = instance.assigned_to
                
                if data['assigned_to'] and data['assigned_to'] != '':
                    try:
                        user = User.objects.get(id=data['assigned_to'])
                        
                        if user.role == 'System Admin':
                            technical_user = User.objects.filter(role='Technical User').first()
                            if technical_user:
                                data['assigned_to'] = technical_user.id
                                user = technical_user
                            else:
                                return Response({'error': 'No Technical Users available for assignment'}, status=status.HTTP_400_BAD_REQUEST)
                        elif user.role not in ['Technical User', 'Technical Supervisor']:
                            return Response({'error': f'User {user.name} ({user.role}) cannot be assigned tickets.'}, status=status.HTTP_400_BAD_REQUEST)
                        
                        # Create notification for assignment
                        if old_assigned_to != data['assigned_to']:
                            Alert.objects.create(
                                user_id=user.id,
                                ticket_id=instance.id,
                                alert_type='assignment',
                                title=f'Ticket Assigned: {instance.ticket_id}',
                                message=f'You have been assigned to ticket {instance.ticket_id}: {instance.title}',
                                is_read=False,
                                created_at=timezone.now()
                            )
                            
                    except User.DoesNotExist:
                        return Response({'error': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    data['assigned_to'] = None
            
            # Handle status change notifications
            old_status = instance.status
            if 'status' in data and data['status'] != old_status:
                if instance.assigned_to:
                    Alert.objects.create(
                        user_id=instance.assigned_to,
                        ticket_id=instance.id,
                        alert_type='status_change',
                        title=f'Status Updated: {instance.ticket_id}',
                        message=f'Ticket {instance.ticket_id} status changed from {old_status} to {data["status"]}',
                        is_read=False,
                        created_at=timezone.now()
                    )
            
            serializer = self.get_serializer(instance, data=data, partial=partial)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            
            # Validate required fields
            required_fields = ['ticket_id', 'sender_id', 'message']
            for field in required_fields:
                if field not in data or not data[field]:
                    return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'OPTIONS'])
@permission_classes([AllowAny])
def health_check(request):
    if request.method == 'OPTIONS':
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    return Response({
        'status': 'healthy',
        'database': 'connected',
        'timestamp': timezone.now().isoformat()
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def ticket_timeline(request, ticket_id):
    return Response([])

@api_view(['GET'])
@permission_classes([AllowAny])
def ticket_activities(request, ticket_id):
    return Response([])

@api_view(['GET'])
@permission_classes([AllowAny])
def ticket_files(request, ticket_id):
    return Response([])

@api_view(['GET'])
@permission_classes([AllowAny])
def export_tickets_excel(request):
    return Response({'message': 'Export not implemented'})

@api_view(['POST'])
@permission_classes([AllowAny])
def assign_ticket(request, ticket_id):
    return Response({'message': 'Assignment not implemented'})

@api_view(['POST'])
@permission_classes([AllowAny])
def auto_assign_ticket(request, ticket_id):
    return Response({'message': 'Auto-assignment not implemented'})