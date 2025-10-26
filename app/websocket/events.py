from flask_socketio import emit, join_room, leave_room, rooms
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app import socketio, db
from app.models.ticket import TicketMessage
from app.websocket import active_connections, user_presence, broadcast_presence_update
from datetime import datetime
import uuid

@socketio.on('connect')
def handle_connect():
    """Handle client connection with enhanced presence tracking"""
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        
        # Track connection
        if user_id not in active_connections:
            active_connections[user_id] = set()
        
        # Update presence
        broadcast_presence_update(user_id, 'online')
        
        emit('connected', {
            'status': 'Connected',
            'user_id': user_id,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Send current presence status
        emit('presence_status', dict(user_presence))
        
    except Exception as e:
        emit('error', {'message': 'Authentication required'})
        return False

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection with cleanup"""
    try:
        user_id = get_jwt_identity()
        
        # Clean up connections
        if user_id in active_connections:
            del active_connections[user_id]
        
        # Update presence
        broadcast_presence_update(user_id, 'offline')
        
        print(f'Client {user_id} disconnected')
    except:
        print('Client disconnected')

@socketio.on('join_ticket')
def handle_join_ticket(data):
    """Join a ticket room for real-time updates"""
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        ticket_id = data.get('ticket_id')
        
        if ticket_id:
            room_name = f'ticket_{ticket_id}'
            join_room(room_name)
            
            # Track room membership
            if user_id in active_connections:
                active_connections[user_id].add(room_name)
            
            emit('joined_ticket', {
                'ticket_id': ticket_id,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            # Notify others in the room
            emit('user_joined_ticket', {
                'user_id': user_id,
                'ticket_id': ticket_id
            }, room=room_name, include_self=False)
            
    except Exception as e:
        emit('error', {'message': 'Failed to join ticket room'})

@socketio.on('leave_ticket')
def handle_leave_ticket(data):
    """Leave a ticket room"""
    try:
        user_id = get_jwt_identity()
        ticket_id = data.get('ticket_id')
        
        if ticket_id:
            room_name = f'ticket_{ticket_id}'
            leave_room(room_name)
            
            # Update room membership
            if user_id in active_connections:
                active_connections[user_id].discard(room_name)
            
            emit('left_ticket', {
                'ticket_id': ticket_id,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            # Notify others in the room
            emit('user_left_ticket', {
                'user_id': user_id,
                'ticket_id': ticket_id
            }, room=room_name, include_self=False)
            
    except Exception as e:
        emit('error', {'message': 'Failed to leave ticket room'})

@socketio.on('send_message')
def handle_send_message(data):
    """Handle real-time message sending with enhanced features"""
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        
        # Create message in database
        message = TicketMessage(
            id=str(uuid.uuid4()),
            ticket_id=data['ticket_id'],
            sender_id=user_id,
            sender_name=data['sender_name'],
            sender_role=data['sender_role'],
            message=data['message'],
            is_internal=data.get('is_internal', False)
        )
        
        db.session.add(message)
        db.session.commit()
        
        # Broadcast to ticket room
        socketio.emit('new_message', {
            'id': message.id,
            'ticket_id': message.ticket_id,
            'sender_id': message.sender_id,
            'sender_name': message.sender_name,
            'sender_role': message.sender_role,
            'message': message.message,
            'is_internal': message.is_internal,
            'timestamp': message.timestamp.isoformat()
        }, room=f'ticket_{data["ticket_id"]}')
        
        # Stop typing indicator
        socketio.emit('user_typing', {
            'ticket_id': data['ticket_id'],
            'user_id': user_id,
            'typing': False
        }, room=f'ticket_{data["ticket_id"]}', include_self=False)
        
    except Exception as e:
        emit('error', {'message': 'Failed to send message'})

@socketio.on('typing_start')
def handle_typing_start(data):
    """Handle typing indicator start with timeout"""
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        ticket_id = data.get('ticket_id')
        user_name = data.get('user_name')
        
        socketio.emit('user_typing', {
            'ticket_id': ticket_id,
            'user_id': user_id,
            'user_name': user_name,
            'typing': True,
            'timestamp': datetime.utcnow().isoformat()
        }, room=f'ticket_{ticket_id}', include_self=False)
        
    except Exception as e:
        emit('error', {'message': 'Failed to send typing indicator'})

@socketio.on('typing_stop')
def handle_typing_stop(data):
    """Handle typing indicator stop"""
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        ticket_id = data.get('ticket_id')
        user_name = data.get('user_name')
        
        socketio.emit('user_typing', {
            'ticket_id': ticket_id,
            'user_id': user_id,
            'user_name': user_name,
            'typing': False,
            'timestamp': datetime.utcnow().isoformat()
        }, room=f'ticket_{ticket_id}', include_self=False)
        
    except Exception as e:
        emit('error', {'message': 'Failed to stop typing indicator'})

@socketio.on('ticket_update')
def handle_ticket_update(data):
    """Handle ticket status/priority updates with validation"""
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        ticket_id = data.get('ticket_id')
        updates = data.get('updates', {})
        
        # Broadcast update to ticket room
        socketio.emit('ticket_updated', {
            'ticket_id': ticket_id,
            'updates': updates,
            'updated_by': user_id,
            'updated_by_name': data.get('updated_by_name'),
            'timestamp': datetime.utcnow().isoformat()
        }, room=f'ticket_{ticket_id}')
        
        # If status changed to resolved/closed, notify
        if 'status' in updates and updates['status'] in ['Resolved', 'Closed']:
            socketio.emit('ticket_status_changed', {
                'ticket_id': ticket_id,
                'new_status': updates['status'],
                'changed_by': data.get('updated_by_name'),
                'timestamp': datetime.utcnow().isoformat()
            }, room=f'ticket_{ticket_id}')
        
    except Exception as e:
        emit('error', {'message': 'Failed to broadcast ticket update'})

@socketio.on('request_presence')
def handle_presence_request():
    """Handle request for current presence status"""
    try:
        verify_jwt_in_request()
        emit('presence_status', dict(user_presence))
    except Exception as e:
        emit('error', {'message': 'Failed to get presence status'})