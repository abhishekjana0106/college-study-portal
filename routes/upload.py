import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from config import Config
from database import query_db, execute_db
from helpers import login_required, log_activity, allowed_file, format_file_size

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    departments = query_db("SELECT * FROM departments WHERE is_active = 1 ORDER BY name ASC")
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        resource_type = request.form.get('resource_type', '').strip()
        department_id = request.form.get('department_id')
        semester = request.form.get('semester')
        subject_id = request.form.get('subject_id')
        academic_year = request.form.get('academic_year', '2025-2026').strip()
        exam_type = request.form.get('exam_type', 'End-Semester').strip()
        tags = request.form.get('tags', '').strip()

        # Validation
        if not title or not resource_type or not department_id or not semester or not subject_id:
            flash('Please complete all mandatory academic fields.', 'warning')
            return render_template('upload.html', departments=departments)

        if 'file' not in request.files:
            flash('No file was selected for upload.', 'danger')
            return render_template('upload.html', departments=departments)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected.', 'warning')
            return render_template('upload.html', departments=departments)

        if not allowed_file(file.filename):
            allowed_list = ', '.join(Config.ALLOWED_EXTENSIONS)
            flash(f'File format not supported. Allowed formats: {allowed_list}', 'danger')
            return render_template('upload.html', departments=departments)

        # Secure file saving
        original_name = secure_filename(file.filename)
        ext = original_name.rsplit('.', 1)[1].lower() if '.' in original_name else 'dat'
        unique_prefix = uuid.uuid4().hex[:12]
        saved_filename = f"{unique_prefix}_{original_name}"
        destination = os.path.join(Config.UPLOAD_FOLDER, saved_filename)
        file.save(destination)

        file_size = os.path.getsize(destination)

        # Role-based approval: Faculty and Admin uploads are automatically approved; Student uploads go to review queue
        user_role = session.get('role', 'student')
        initial_status = 'approved' if user_role in ('admin', 'faculty') else 'pending'

        res_id = execute_db("""
            INSERT INTO resources (
                title, description, resource_type, department_id, semester, subject_id,
                academic_year, exam_type, file_name, original_file_name, file_size,
                file_ext, uploader_id, status, tags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            title, description, resource_type, int(department_id), int(semester), int(subject_id),
            academic_year, exam_type, saved_filename, original_name, file_size,
            ext, session['user_id'], initial_status, tags
        ))

        log_activity(
            session['user_id'],
            'UPLOAD_RESOURCE',
            f"Uploaded resource '{title}' (ID: {res_id}, Status: {initial_status})"
        )

        if initial_status == 'approved':
            flash('Resource uploaded and published successfully!', 'success')
            return redirect(url_for('main.resource_detail', resource_id=res_id))
        else:
            flash('Resource uploaded successfully! It is now in the review queue and will be published once approved by faculty or an administrator.', 'info')
            return redirect(url_for('upload.my_uploads'))

    return render_template('upload.html', departments=departments)

@upload_bp.route('/my-uploads')
@login_required
def my_uploads():
    user_id = session['user_id']
    resources = query_db("""
        SELECT r.*, d.name as department_name, d.code as department_code, s.name as subject_name
        FROM resources r
        JOIN departments d ON r.department_id = d.id
        JOIN subjects s ON r.subject_id = s.id
        WHERE r.uploader_id = ?
        ORDER BY r.created_at DESC
    """, (user_id,))

    counts = {
        'total': len(resources),
        'approved': sum(1 for r in resources if r['status'] == 'approved'),
        'pending': sum(1 for r in resources if r['status'] == 'pending'),
        'rejected': sum(1 for r in resources if r['status'] == 'rejected')
    }

    return render_template('my_uploads.html', resources=resources, counts=counts, format_file_size=format_file_size)

@upload_bp.route('/delete-my-upload/<int:resource_id>', methods=['POST'])
@login_required
def delete_my_upload(resource_id):
    user_id = session['user_id']
    res = query_db("SELECT * FROM resources WHERE id = ? AND uploader_id = ?", (resource_id, user_id), one=True)
    if not res:
        flash('Resource not found or unauthorized.', 'danger')
        return redirect(url_for('upload.my_uploads'))

    # Remove physical file if exists
    filepath = os.path.join(Config.UPLOAD_FOLDER, res['file_name'])
    if os.path.isfile(filepath):
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Error deleting file {filepath}: {e}")

    execute_db("DELETE FROM resources WHERE id = ?", (resource_id,))
    log_activity(user_id, 'DELETE_MY_RESOURCE', f"Deleted resource: {res['title']}")
    flash('Resource deleted successfully.', 'success')
    return redirect(url_for('upload.my_uploads'))
