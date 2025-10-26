# ServiceDesk Backend

A Flask-based backend for a service desk ticketing system with real-time WebSocket communication.

## Project Structure

```
servicedesk-backend/
├── app/
│   ├── models/           # Database models
│   │   ├── user.py       # Agent model
│   │   ├── ticket.py     # Ticket and TicketMessage models
│   │   └── attachment.py # File attachment model
│   ├── routes/           # API endpoints
│   │   ├── tickets.py    # Ticket workflow endpoints
│   │   └── files.py      # File upload/download endpoints
│   ├── services/         # Business logic
│   │   └── assignment_service.py  # Ticket assignment logic
│   ├── websocket/        # Real-time communication
│   │   ├── __init__.py   # WebSocket configuration
│   │   └── events.py     # WebSocket event handlers
│   └── __init__.py       # App factory
├── app.py               # Application entry point
├── config.py            # Configuration classes
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Features

### Branch 1: WebSocket Enhancement (DESK-301)
- ✅ Real-time ticket updates
- ✅ Presence indicators
- ✅ Typing indicators
- ✅ Reconnection logic
- ✅ Enhanced WebSocket setup

### Branch 2: Ticket Workflow (DESK-302)
- ✅ Ticket status transitions with validation
- ✅ Auto-assignment rules with scoring
- ✅ Escalation logic
- ✅ Workflow validation
- ✅ Enhanced assignment service

### Branch 3: File Management (DESK-303)
- ✅ Enhanced file upload/download
- ✅ File type validation
- ✅ File preview and thumbnails
- ✅ Drag-and-drop support (backend ready)
- ✅ File size limits and validation

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables (optional):
```bash
export FLASK_ENV=development
export SECRET_KEY=your-secret-key
export JWT_SECRET_KEY=your-jwt-secret
```

3. Run the application:
```bash
python app.py
```

## API Endpoints

### Tickets
- `GET /api/tickets/` - Get all tickets with filtering
- `POST /api/tickets/` - Create new ticket with auto-assignment
- `GET /api/tickets/<id>` - Get specific ticket
- `PUT /api/tickets/<id>/status` - Update ticket status
- `PUT /api/tickets/<id>/priority` - Update ticket priority
- `PUT /api/tickets/<id>/assign` - Assign ticket to agent
- `POST /api/tickets/<id>/escalate` - Escalate ticket
- `GET /api/tickets/workflow/transitions` - Get workflow rules
- `GET /api/tickets/stats` - Get ticket statistics

### Files
- `POST /api/files/upload` - Upload file with validation
- `GET /api/files/<id>/download` - Download file
- `GET /api/files/<id>/thumbnail` - Get image thumbnail
- `GET /api/files/<id>/preview` - Get file preview
- `GET /api/files/ticket/<id>` - Get all files for ticket
- `DELETE /api/files/<id>` - Delete file
- `POST /api/files/validate` - Validate files before upload

## WebSocket Events

### Client to Server
- `connect` - Establish connection
- `join_ticket` - Join ticket room
- `leave_ticket` - Leave ticket room
- `send_message` - Send message
- `typing_start/stop` - Typing indicators
- `ticket_update` - Broadcast ticket updates

### Server to Client
- `connected` - Connection confirmed
- `new_message` - New message received
- `user_typing` - User typing status
- `ticket_updated` - Ticket was updated
- `presence_update` - User presence changed
- `file_uploaded` - File was uploaded

## Configuration

The application supports multiple environments through `config.py`:
- Development: Debug enabled, SQLite database
- Production: Debug disabled, optimized settings
- Testing: In-memory database for tests

## Next Steps

1. **Frontend Integration**: Connect React components to these APIs
2. **Authentication**: Implement user authentication system
3. **Database Migration**: Set up proper database with migrations
4. **Testing**: Add comprehensive test suite
5. **Deployment**: Configure for production deployment