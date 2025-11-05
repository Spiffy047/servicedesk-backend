from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from tickets.models import Ticket
from users.models import User

@api_view(['GET'])
@permission_classes([AllowAny])
def sla_adherence(request):
    try:
        total_tickets = Ticket.objects.count()
        violations = Ticket.objects.filter(sla_violated=True).count()
        on_time = total_tickets - violations
        sla_adherence = (on_time / total_tickets * 100) if total_tickets > 0 else 0
        
        return Response({
            'sla_adherence': round(sla_adherence, 1),
            'total_tickets': total_tickets,
            'violations': violations,
            'on_time': on_time,
            'trend': 'stable'
        })
    except Exception as e:
        return Response({
            'sla_adherence': 0,
            'total_tickets': 0,
            'violations': 0,
            'on_time': 0,
            'trend': 'stable'
        })

@api_view(['GET'])
@permission_classes([AllowAny])
def agent_performance(request):
    try:
        agents = User.objects.filter(role__in=['Technical User', 'Technical Supervisor'])
        performance_data = []
        
        for agent in agents:
            closed_tickets = Ticket.objects.filter(
                assigned_to=agent.id,
                status__in=['Resolved', 'Closed']
            ).count()
            
            sla_violations = Ticket.objects.filter(
                assigned_to=agent.id,
                sla_violated=True
            ).count()
            
            performance_data.append({
                'id': agent.id,
                'name': agent.name,
                'tickets_closed': closed_tickets,
                'avg_handle_time': 24.5,
                'sla_violations': sla_violations,
                'rating': 'Good' if closed_tickets > 5 else 'Average'
            })
        
        return Response(performance_data)
    except Exception as e:
        return Response([])

@api_view(['GET'])
@permission_classes([AllowAny])
def ticket_status_counts(request):
    try:
        counts = {
            'new': Ticket.objects.filter(status='New').count(),
            'open': Ticket.objects.filter(status__in=['Open', 'In Progress']).count(),
            'pending': Ticket.objects.filter(status='Pending').count(),
            'closed': Ticket.objects.filter(status__in=['Resolved', 'Closed']).count()
        }
        return Response(counts)
    except Exception as e:
        return Response({'new': 0, 'open': 0, 'pending': 0, 'closed': 0})

@api_view(['GET', 'OPTIONS'])
@permission_classes([AllowAny])
def agent_workload(request):
    if request.method == 'OPTIONS':
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    try:
        agents = User.objects.filter(role__in=['Technical User', 'Technical Supervisor'])
        workload_data = []
        
        for agent in agents:
            total_tickets = Ticket.objects.filter(assigned_to=agent.id).count()
            active_tickets = Ticket.objects.filter(
                assigned_to=agent.id,
                status__in=['New', 'Open', 'In Progress', 'Pending']
            ).count()
            
            workload_data.append({
                'agent_id': agent.id,
                'id': agent.id,
                'name': agent.name,
                'email': agent.email,
                'role': agent.role,
                'ticket_count': total_tickets,
                'active_tickets': active_tickets
            })
        
        return Response(workload_data)
    except Exception as e:
        return Response([])

@api_view(['GET'])
@permission_classes([AllowAny])
def unassigned_tickets(request):
    try:
        tickets = Ticket.objects.filter(
            assigned_to__isnull=True,
            status__in=['New', 'Open']
        )[:20]
        
        ticket_data = []
        for ticket in tickets:
            ticket_data.append({
                'id': ticket.ticket_id,
                'ticket_id': ticket.ticket_id,
                'title': ticket.title,
                'priority': ticket.priority,
                'category': ticket.category,
                'status': ticket.status,
                'created_at': ticket.created_at.isoformat() if ticket.created_at else None,
                'hours_open': 0
            })
        
        return Response({'tickets': ticket_data})
    except Exception as e:
        return Response({'tickets': []})

@api_view(['GET'])
@permission_classes([AllowAny])
def ticket_aging(request):
    try:
        tickets = Ticket.objects.filter(status__ne='Closed')
        aging_buckets = {
            '0-24h': [],
            '24-48h': [],
            '48-72h': [],
            '72h+': []
        }
        
        return Response({
            'aging_data': [
                {'age_range': '0-24h', 'count': 0},
                {'age_range': '24-48h', 'count': 0},
                {'age_range': '48-72h', 'count': 0},
                {'age_range': '72h+', 'count': 0}
            ],
            'buckets': aging_buckets,
            'total_open_tickets': 0,
            'average_age_hours': 0
        })
    except Exception as e:
        return Response({
            'aging_data': [
                {'age_range': '0-24h', 'count': 0},
                {'age_range': '24-48h', 'count': 0},
                {'age_range': '48-72h', 'count': 0},
                {'age_range': '72h+', 'count': 0}
            ],
            'buckets': {'0-24h': [], '24-48h': [], '48-72h': [], '72h+': []},
            'total_open_tickets': 0,
            'average_age_hours': 0
        })