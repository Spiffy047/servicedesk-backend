from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from app import db, socketio
from app.models.attachment import FileAttachment
from app.models.ticket import Ticket
import os
import uuid
import mimetypes
from datetime import datetime
from PIL import Image
import magic

files_bp = Blueprint('files', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads')
THUMBNAIL_FOLDER = os.path.join(UPLOAD_FOLDER, 'thumbnails')

# Enhanced file type validation
ALLOWED_EXTENSIONS = {
    'documents': {'txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'rtf'},
    'images': {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'svg'},
    'archives': {'zip', 'rar', '7z', 'tar', 'gz'},
    'logs': {'log', 'txt', 'csv'},
    'code': {'py', 'js', 'html', 'css', 'json', 'xml', 'sql'}
}

ALL_ALLOWED = set().union(*ALLOWED_EXTENSIONS.values())
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB for images

# Create directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(THUMBNAIL_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALL_ALLOWED

def get_file_category(filename):
    """Get file category based on extension"""
    if not filename or '.' not in filename:
        return 'unknown'
    
    ext = filename.rsplit('.', 1)[1].lower()
    for category, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return category
    return 'unknown'

def validate_file_content(file_path, expected_mime):
    """Validate file content matches extension using python-magic"""
    try:
        mime = magic.Magic(mime=True)
        actual_mime = mime.from_file(file_path)
        
        # Basic validation - check if MIME types are compatible
        if expected_mime.startswith('image/') and not actual_mime.startswith('image/'):
            return False
        if expected_mime.startswith('text/') and not actual_mime.startswith('text/'):
            return False
            
        return True
    except:
        return True  # If validation fails, allow the file

def create_thumbnail(image_path, thumbnail_path, size=(150, 150)):
    """Create thumbnail for image files"""
    try:
        with Image.open(image_path) as img:
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(thumbnail_path, 'JPEG', quality=85)
            return True
    except Exception as e:
        print(f"Thumbnail creation failed: {e}")
        return False

@files_bp.route('/upload', methods=['POST'])
def upload_file():
    """Enhanced file upload with validation and thumbnails"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    ticket_id = request.form.get('ticket_id')
    message_id = request.form.get('message_id')
    uploaded_by = request.form.get('uploaded_by')
    
    if not ticket_id or not uploaded_by:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            'error': 'File type not allowed',
            'allowed_types': list(ALL_ALLOWED)
        }), 400
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    category = get_file_category(file.filename)
    max_size = MAX_IMAGE_SIZE if category == 'images' else MAX_FILE_SIZE
    
    if file_size > max_size:
        return jsonify({
            'error': f'File too large. Maximum size: {max_size // (1024*1024)}MB'
        }), 400
    
    # Secure filename and create unique path
    original_filename = secure_filename(file.filename)
    file_id = str(uuid.uuid4())
    filename = f"{file_id}_{original_filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    # Save file
    file.save(filepath)
    
    # Validate file content
    mime_type = file.content_type or mimetypes.guess_type(original_filename)[0] or 'application/octet-stream'
    
    if not validate_file_content(filepath, mime_type):
        os.remove(filepath)
        return jsonify({'error': 'File content does not match extension'}), 400
    
    # Create thumbnail for images
    thumbnail_path = None
    if category == 'images':
        thumbnail_filename = f"thumb_{file_id}.jpg"
        thumbnail_path = os.path.join(THUMBNAIL_FOLDER, thumbnail_filename)
        create_thumbnail(filepath, thumbnail_path)
    
    # Create attachment record
    attachment = FileAttachment(
        id=file_id,
        ticket_id=ticket_id,
        message_id=message_id,
        filename=filename,
        original_filename=original_filename,
        file_size=file_size,
        mime_type=mime_type,
        storage_path=filepath,
        uploaded_by=uploaded_by,
        is_scanned=True,
        scan_result='clean'
    )
    
    db.session.add(attachment)
    db.session.commit()
    
    # Broadcast file upload event
    socketio.emit('file_uploaded', {
        'ticket_id': ticket_id,
        'file_id': file_id,
        'filename': original_filename,
        'uploaded_by': uploaded_by,
        'file_size_mb': attachment.file_size_mb,
        'category': category
    }, room=f'ticket_{ticket_id}')
    
    response_data = {
        'id': attachment.id,
        'filename': attachment.original_filename,
        'file_size_mb': attachment.file_size_mb,
        'mime_type': attachment.mime_type,
        'category': category,
        'uploaded_at': attachment.uploaded_at.isoformat(),
        'download_url': f'/api/files/{attachment.id}/download'
    }
    
    if thumbnail_path and os.path.exists(thumbnail_path):
        response_data['thumbnail_url'] = f'/api/files/{attachment.id}/thumbnail'
    
    return jsonify(response_data), 201

@files_bp.route('/<file_id>/download', methods=['GET'])
def download_file(file_id):
    """Download file with security checks"""
    attachment = FileAttachment.query.get_or_404(file_id)
    
    if not os.path.exists(attachment.storage_path):
        return jsonify({'error': 'File not found on disk'}), 404
    
    return send_file(
        attachment.storage_path,
        as_attachment=True,
        download_name=attachment.original_filename,
        mimetype=attachment.mime_type
    )

@files_bp.route('/<file_id>/thumbnail', methods=['GET'])
def get_thumbnail(file_id):
    """Get thumbnail for image files"""
    attachment = FileAttachment.query.get_or_404(file_id)
    
    thumbnail_filename = f"thumb_{file_id}.jpg"
    thumbnail_path = os.path.join(THUMBNAIL_FOLDER, thumbnail_filename)
    
    if not os.path.exists(thumbnail_path):
        # Try to create thumbnail if it doesn't exist
        if get_file_category(attachment.original_filename) == 'images':
            if create_thumbnail(attachment.storage_path, thumbnail_path):
                return send_file(thumbnail_path, mimetype='image/jpeg')
        return jsonify({'error': 'Thumbnail not available'}), 404
    
    return send_file(thumbnail_path, mimetype='image/jpeg')

@files_bp.route('/<file_id>/preview', methods=['GET'])
def preview_file(file_id):
    """Get file preview information"""
    attachment = FileAttachment.query.get_or_404(file_id)
    category = get_file_category(attachment.original_filename)
    
    preview_data = {
        'id': attachment.id,
        'filename': attachment.original_filename,
        'file_size_mb': attachment.file_size_mb,
        'mime_type': attachment.mime_type,
        'category': category,
        'uploaded_at': attachment.uploaded_at.isoformat(),
        'can_preview': category in ['images', 'documents']
    }
    
    # Add thumbnail URL for images
    if category == 'images':
        thumbnail_path = os.path.join(THUMBNAIL_FOLDER, f"thumb_{file_id}.jpg")
        if os.path.exists(thumbnail_path):
            preview_data['thumbnail_url'] = f'/api/files/{file_id}/thumbnail'
    
    # Add text preview for small text files
    if category in ['logs', 'code'] and attachment.file_size < 1024 * 1024:  # 1MB limit
        try:
            with open(attachment.storage_path, 'r', encoding='utf-8') as f:
                preview_data['text_preview'] = f.read(5000)  # First 5000 chars
        except:
            pass
    
    return jsonify(preview_data)

@files_bp.route('/ticket/<ticket_id>', methods=['GET'])
def get_ticket_files(ticket_id):
    """Get all files for a ticket with enhanced metadata"""
    attachments = FileAttachment.query.filter_by(ticket_id=ticket_id).order_by(FileAttachment.uploaded_at.desc()).all()
    
    files_data = []
    for a in attachments:
        category = get_file_category(a.original_filename)
        file_data = {
            'id': a.id,
            'filename': a.original_filename,
            'file_size_mb': a.file_size_mb,
            'mime_type': a.mime_type,
            'category': category,
            'uploaded_by': a.uploaded_by,
            'uploaded_at': a.uploaded_at.isoformat(),
            'download_url': f'/api/files/{a.id}/download',
            'preview_url': f'/api/files/{a.id}/preview'
        }
        
        # Add thumbnail URL for images
        if category == 'images':
            thumbnail_path = os.path.join(THUMBNAIL_FOLDER, f"thumb_{a.id}.jpg")
            if os.path.exists(thumbnail_path):
                file_data['thumbnail_url'] = f'/api/files/{a.id}/thumbnail'
        
        files_data.append(file_data)
    
    return jsonify(files_data)

@files_bp.route('/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    """Delete a file attachment"""
    attachment = FileAttachment.query.get_or_404(file_id)
    
    # Remove file from disk
    if os.path.exists(attachment.storage_path):
        os.remove(attachment.storage_path)
    
    # Remove thumbnail if exists
    thumbnail_path = os.path.join(THUMBNAIL_FOLDER, f"thumb_{file_id}.jpg")
    if os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)
    
    # Remove from database
    db.session.delete(attachment)
    db.session.commit()
    
    # Broadcast file deletion
    socketio.emit('file_deleted', {
        'ticket_id': attachment.ticket_id,
        'file_id': file_id,
        'filename': attachment.original_filename
    }, room=f'ticket_{attachment.ticket_id}')
    
    return jsonify({'message': 'File deleted successfully'})

@files_bp.route('/validate', methods=['POST'])
def validate_files():
    """Validate multiple files before upload"""
    files = request.files.getlist('files')
    
    if not files:
        return jsonify({'error': 'No files provided'}), 400
    
    validation_results = []
    total_size = 0
    
    for file in files:
        if file.filename == '':
            continue
            
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        total_size += file_size
        category = get_file_category(file.filename)
        max_size = MAX_IMAGE_SIZE if category == 'images' else MAX_FILE_SIZE
        
        result = {
            'filename': file.filename,
            'size': file_size,
            'size_mb': round(file_size / (1024 * 1024), 2),
            'category': category,
            'valid': True,
            'errors': []
        }
        
        if not allowed_file(file.filename):
            result['valid'] = False
            result['errors'].append('File type not allowed')
        
        if file_size > max_size:
            result['valid'] = False
            result['errors'].append(f'File too large (max: {max_size // (1024*1024)}MB)')
        
        validation_results.append(result)
    
    return jsonify({
        'files': validation_results,
        'total_size_mb': round(total_size / (1024 * 1024), 2),
        'valid_files': len([r for r in validation_results if r['valid']]),
        'total_files': len(validation_results)
    })

