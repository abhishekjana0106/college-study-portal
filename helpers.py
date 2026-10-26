import os
from functools import wraps
from flask import session, redirect, url_for, flash, request, g
from config import Config
from database import query_db, execute_db

def get_current_user():
    """Retrieve logged in user information."""
    user_id = session.get('user_id')
    if not user_id:
        return None
    user = query_db(
        """SELECT u.*, d.name as department_name, d.code as department_code 
           FROM users u 
           LEFT JOIN departments d ON u.department_id = d.id 
           WHERE u.id = ? AND u.is_active = 1""", 
        (user_id,), 
        one=True
    )
    return user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to access the administrator panel.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        if session.get('role') != 'admin':
            flash('Access denied. Administrator privileges required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def faculty_or_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        if session.get('role') not in ('admin', 'faculty'):
            flash('Access restricted to faculty and administrators.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def format_file_size(size_bytes):
    """Format file size in human readable format."""
    if not size_bytes or size_bytes <= 0:
        return "0 KB"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}" if unit != 'B' else f"{int(size_bytes)} B"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def log_activity(user_id, action, details):
    """Record audit log into the activity_logs table."""
    try:
        ip = request.remote_addr if request else '127.0.0.1'
        execute_db(
            "INSERT INTO activity_logs (user_id, action, details, ip_address) VALUES (?, ?, ?, ?)",
            (user_id, action, details, ip)
        )
    except Exception as e:
        print(f"Failed to log activity: {e}")
