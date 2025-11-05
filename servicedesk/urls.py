from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, login_view, me_view
from tickets.views import TicketViewSet, MessageViewSet, health_check
from notifications.views import (
    alert_count, user_alerts, notification_count, user_notifications,
    mark_notification_read, mark_all_notifications_read, create_notification
)
from analytics.views import (
    sla_adherence, agent_performance, ticket_status_counts, 
    agent_workload, unassigned_tickets, ticket_aging
)
from tickets.views import ticket_timeline, ticket_activities, ticket_files, export_tickets_excel, assign_ticket, auto_assign_ticket
from users.views import assignable_users
from files.views import upload_file, upload_image

router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health', health_check, name='health'),
    
    # Assignable users endpoint (before router to avoid conflicts)
    path('api/users/assignable', assignable_users, name='assignable_users'),
    path('api/users/assignable/', assignable_users, name='assignable_users_slash'),
    
    path('api/', include(router.urls)),
    
    # Auth endpoints (with and without trailing slashes)
    path('api/auth/login', login_view, name='login'),
    path('api/auth/login/', login_view, name='login_slash'),
    path('api/auth/me', me_view, name='me'),
    path('api/auth/me/', me_view, name='me_slash'),
    
    # Analytics endpoints (with and without trailing slashes)
    path('api/analytics/sla-adherence', sla_adherence, name='sla_adherence'),
    path('api/analytics/sla-adherence/', sla_adherence, name='sla_adherence_slash'),
    path('api/analytics/agent-performance', agent_performance, name='agent_performance'),
    path('api/analytics/agent-performance/', agent_performance, name='agent_performance_slash'),
    path('api/analytics/ticket-status-counts', ticket_status_counts, name='ticket_status_counts'),
    path('api/analytics/ticket-status-counts/', ticket_status_counts, name='ticket_status_counts_slash'),
    path('api/analytics/agent-workload', agent_workload, name='agent_workload'),
    path('api/analytics/agent-workload/', agent_workload, name='agent_workload_slash'),
    path('api/analytics/unassigned-tickets', unassigned_tickets, name='unassigned_tickets'),
    path('api/analytics/unassigned-tickets/', unassigned_tickets, name='unassigned_tickets_slash'),
    path('api/analytics/ticket-aging', ticket_aging, name='ticket_aging'),
    path('api/analytics/ticket-aging/', ticket_aging, name='ticket_aging_slash'),
    
    # Analytics endpoints with /tickets/ prefix (frontend calls these)
    path('api/tickets/analytics/sla-adherence', sla_adherence, name='tickets_sla_adherence'),
    path('api/tickets/analytics/sla-adherence/', sla_adherence, name='tickets_sla_adherence_slash'),
    path('api/tickets/analytics/agent-performance', agent_performance, name='tickets_agent_performance'),
    path('api/tickets/analytics/agent-performance/', agent_performance, name='tickets_agent_performance_slash'),
    path('api/tickets/analytics/ticket-status-counts', ticket_status_counts, name='tickets_ticket_status_counts'),
    path('api/tickets/analytics/ticket-status-counts/', ticket_status_counts, name='tickets_ticket_status_counts_slash'),
    path('api/tickets/analytics/agent-workload', agent_workload, name='tickets_agent_workload'),
    path('api/tickets/analytics/agent-workload/', agent_workload, name='tickets_agent_workload_slash'),
    path('api/tickets/analytics/unassigned-tickets', unassigned_tickets, name='tickets_unassigned_tickets'),
    path('api/tickets/analytics/unassigned-tickets/', unassigned_tickets, name='tickets_unassigned_tickets_slash'),
    path('api/tickets/analytics/ticket-aging', ticket_aging, name='tickets_ticket_aging'),
    path('api/tickets/analytics/ticket-aging/', ticket_aging, name='tickets_ticket_aging_slash'),
    
    # Notification Bell endpoints
    path('api/notifications/<int:user_id>/count', notification_count, name='notification_count'),
    path('api/notifications/<int:user_id>/count/', notification_count, name='notification_count_slash'),
    path('api/notifications/<int:user_id>', user_notifications, name='user_notifications'),
    path('api/notifications/<int:user_id>/', user_notifications, name='user_notifications_slash'),
    path('api/notifications/<int:notification_id>/read', mark_notification_read, name='mark_notification_read'),
    path('api/notifications/<int:notification_id>/read/', mark_notification_read, name='mark_notification_read_slash'),
    path('api/notifications/<int:user_id>/read-all', mark_all_notifications_read, name='mark_all_notifications_read'),
    path('api/notifications/<int:user_id>/read-all/', mark_all_notifications_read, name='mark_all_notifications_read_slash'),
    path('api/notifications/create', create_notification, name='create_notification'),
    path('api/notifications/create/', create_notification, name='create_notification_slash'),
    
    # Alert endpoints (legacy - with and without trailing slashes)
    path('api/alerts/<int:user_id>/count', alert_count, name='alert_count'),
    path('api/alerts/<int:user_id>/count/', alert_count, name='alert_count_slash'),
    path('api/alerts/<int:user_id>', user_alerts, name='user_alerts'),
    path('api/alerts/<int:user_id>/', user_alerts, name='user_alerts_slash'),
    
    # Agent endpoints (with and without trailing slashes)
    path('api/agents/assignable', agent_performance, name='assignable_agents'),
    path('api/agents/assignable/', agent_performance, name='assignable_agents_slash'),
    
    # Missing ticket endpoints
    path('api/messages/ticket/<str:ticket_id>/timeline', ticket_timeline, name='ticket_timeline'),
    path('api/tickets/<int:ticket_id>/activities', ticket_activities, name='ticket_activities'),
    path('api/files/ticket/<int:ticket_id>', ticket_files, name='ticket_files'),
    
    # Export endpoints
    path('api/export/tickets/excel', export_tickets_excel, name='export_tickets_excel'),
    path('api/export/tickets/excel/', export_tickets_excel, name='export_tickets_excel_slash'),
    
    # Ticket assignment endpoint
    path('api/tickets/<int:ticket_id>/assign', assign_ticket, name='assign_ticket'),
    path('api/tickets/<int:ticket_id>/assign/', assign_ticket, name='assign_ticket_slash'),
    
    # Auto-assign endpoint (assigns to first available Technical User)
    path('api/tickets/<int:ticket_id>/auto-assign', auto_assign_ticket, name='auto_assign_ticket'),
    path('api/tickets/<int:ticket_id>/auto-assign/', auto_assign_ticket, name='auto_assign_ticket_slash'),
    
    # File upload endpoints
    path('api/files/upload', upload_file, name='upload_file'),
    path('api/files/upload/', upload_file, name='upload_file_slash'),
    path('api/upload/image', upload_image, name='upload_image'),
    path('api/upload/image/', upload_image, name='upload_image_slash'),
]