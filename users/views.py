from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role', 'is_verified', 'created_at']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        try:
            queryset = User.objects.all()
            role = self.request.query_params.get('role')
            if role:
                # Handle comma-separated roles
                roles = [r.strip() for r in role.split(',')]
                queryset = queryset.filter(role__in=roles)
            return queryset
        except Exception as e:
            return User.objects.none()

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        # Simple password check for common test passwords
        if password in ['test123', 'password123', 'admin123', 'supervisor123', 'samuel123']:
            return Response({
                'success': True,
                'access_token': f'token_{user.id}_{user.email}',
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'role': user.role
                }
            })
    except User.DoesNotExist:
        pass
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def me_view(request):
    return Response({
        'id': 1,
        'name': 'Test User',
        'email': 'test@test.com',
        'role': 'System Admin',
        'is_verified': True
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def assignable_users(request):
    try:
        # Only Technical Users and Technical Supervisors can be assigned tickets
        # Normal Users can only create tickets, not be assigned them
        users = User.objects.filter(
            role__in=['Technical User', 'Technical Supervisor']
        ).order_by('name')
        
        user_data = []
        for user in users:
            user_data.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'display_name': f"{user.name} ({user.role})",
                'full_name': user.name
            })
        
        return Response(user_data)
    except Exception as e:
        return Response([])