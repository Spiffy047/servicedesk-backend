from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from .models import Alert
from users.models import User
from tickets.models import Ticket

@api_view(['GET'])
@permission_classes([AllowAny])
def notification_count(request, user_id):
    """Get unread notification count for notification bell"""
    try:
        count = Alert.objects.filter(user_id=user_id, is_read=False).count()
        return Response({'count': count, 'has_notifications': count > 0})
    except Exception as e:
        return Response({'count': 0, 'has_notifications': False})

@api_view(['GET'])
@permission_classes([AllowAny])
def user_notifications(request, user_id):
    """Get user notifications for notification dropdown"""
    try:
        alerts = Alert.objects.filter(user_id=user_id).order_by('-created_at')[:20]
        notifications = []
        
        for alert in alerts:
            # Get ticket info if available
            ticket_info = None
            try:
                ticket = Ticket.objects.get(id=alert.ticket_id)
                ticket_info = {
                    'ticket_id': ticket.ticket_id,
                    'title': ticket.title
                }
            except Ticket.DoesNotExist:
                pass
            
            notifications.append({
                'id': alert.id,
                'title': alert.title,
                'message': alert.message,
                'type': alert.alert_type,
                'is_read': alert.is_read,
                'created_at': alert.created_at.isoformat() if alert.created_at else None,
                'ticket_id': alert.ticket_id,
                'ticket_info': ticket_info,
                'time_ago': get_time_ago(alert.created_at)
            })
        
        return Response({
            'notifications': notifications,
            'unread_count': Alert.objects.filter(user_id=user_id, is_read=False).count()
        })
    except Exception as e:
        return Response({'notifications': [], 'unread_count': 0})

@api_view(['POST'])
@permission_classes([AllowAny])
def mark_notification_read(request, notification_id):
    """Mark a specific notification as read"""
    try:
        alert = Alert.objects.get(id=notification_id)
        alert.is_read = True
        alert.save()
        return Response({'success': True, 'message': 'Notification marked as read'})
    except Alert.DoesNotExist:
        return Response({'success': False, 'message': 'Notification not found'}, status=404)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def mark_all_notifications_read(request, user_id):
    """Mark all notifications as read for a user"""
    try:
        Alert.objects.filter(user_id=user_id, is_read=False).update(is_read=True)
        return Response({'success': True, 'message': 'All notifications marked as read'})
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_notification(request):
    """Create a new notification"""
    try:
        data = request.data
        alert = Alert.objects.create(
            user_id=data['user_id'],
            ticket_id=data.get('ticket_id', 0),
            alert_type=data.get('alert_type', 'assignment'),
            title=data['title'],
            message=data['message'],
            is_read=False,
            created_at=timezone.now()
        )
        return Response({
            'success': True, 
            'notification_id': alert.id,
            'message': 'Notification created successfully'
        })
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=500)

def get_time_ago(created_at):
    """Helper function to get human-readable time ago"""
    if not created_at:
        return 'Unknown'
    
    now = timezone.now()
    diff = now - created_at
    
    if diff.days > 0:
        return f'{diff.days} day{"s" if diff.days > 1 else ""} ago'
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f'{hours} hour{"s" if hours > 1 else ""} ago'
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f'{minutes} minute{"s" if minutes > 1 else ""} ago'
    else:
        return 'Just now'

# Legacy endpoints for backward compatibility
alert_count = notification_count
user_alerts = user_notifications