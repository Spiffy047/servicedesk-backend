from flask_socketio import SocketIO
from app import socketio
from datetime import datetime

# WebSocket configuration
WEBSOCKET_CONFIG = {
    'cors_allowed_origins': "*",
    'async_mode': 'threading',
    'ping_timeout': 60,
    'ping_interval': 25
}

# Connection tracking
active_connections = {}
user_presence = {}

def init_websocket(app):
    """Initialize WebSocket with enhanced configuration"""
    socketio.init_app(app, **WEBSOCKET_CONFIG)
    return socketio

def broadcast_to_ticket(ticket_id, event, data):
    """Broadcast event to all users in a ticket room"""
    socketio.emit(event, data, room=f'ticket_{ticket_id}')

def broadcast_presence_update(user_id, status):
    """Broadcast user presence update"""
    user_presence[user_id] = status
    socketio.emit('presence_update', {
        'user_id': user_id,
        'status': status,
        'timestamp': datetime.utcnow().isoformat()
    }, broadcast=True)

def get_active_users_in_ticket(ticket_id):
    """Get list of active users in a ticket room"""
    room_name = f'ticket_{ticket_id}'
    return [user for user, rooms in active_connections.items() if room_name in rooms]