import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    BASE_DIR = BASE_DIR
    SECRET_KEY = os.environ.get('SECRET_KEY', 'college-study-portal-secret-key-2026-supersecure')
    DATABASE = os.path.join(BASE_DIR, 'portal.db')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 64 * 1024 * 1024  # 64 MB maximum upload size
    ALLOWED_EXTENSIONS = {
        'pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx',
        'txt', 'zip', 'rar', 'jpg', 'jpeg', 'png'
    }
    PORT = int(os.environ.get('PORT', 5000))
    HOST = os.environ.get('HOST', '0.0.0.0')  # Listen on all interfaces for LAN & offline access
