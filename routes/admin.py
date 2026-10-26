import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from config import Config
from database import query_db, execute_db
from helpers import admin_required, log_activity, format_file_size

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@admin_required
def dashboard():
    stats = {
        'total_resources': query_db("SELECT COUNT(*) as c FROM resources", one=True)['c'],
        'approved_resources': query_db("SELECT COUNT(*) as c FROM resources WHERE status = 'approved'", one=True)['c'],
        'pending_resources': query_db("SELECT COUNT(*) as c FROM resources WHERE status = 'pending'", one=True)['c'],
        'total_downloads': query_db("SELECT COALESCE(SUM(download_count), 0) as c FROM resources", one=True)['c'],
        'total_users': query_db("SELECT COUNT(*) as c FROM users", one=True)['c'],
        'total_departments': query_db("SELECT COUNT(*) as c FROM departments", one=True)['c'],
        'total_subjects': query_db("SELECT COUNT(*) as c FROM subjects", one=True)['c']
    }

    # Pending uploads for immediate action
    pending_items = query_db("""
        SELECT r.*, d.name as department_name, d.code as department_code, s.name as subject_name,
               u.full_name as uploader_name, u.username as uploader_username, u.role as uploader_role
        FROM resources r
        JOIN departments d ON r.department_id = d.id
        JOIN subjects s ON r.subject_id = s.id
        LEFT JOIN users u ON r.uploader_id = u.id
        WHERE r.status = 'pending'
        ORDER BY r.created_at ASC
        LIMIT 6
    """)

    # Breakdown by resource type
    type_breakdown = query_db("""
        SELECT resource_type, COUNT(*) as count
        FROM resources
        GROUP BY resource_type
        ORDER BY count DESC
    """)

    # Breakdown by department
    dept_breakdown = query_db("""
        SELECT d.code, d.name, COUNT(r.id) as count
        FROM departments d
        LEFT JOIN resources r ON d.id = r.department_id
        GROUP BY d.id
        ORDER BY count DESC
        LIMIT 6
    """)

    # Recent Audit Logs
    recent_logs = query_db("""
        SELECT l.*, u.username, u.full_name, u.role
        FROM activity_logs l
        LEFT JOIN users u ON l.user_id = u.id
        ORDER BY l.created_at DESC
        LIMIT 8
    """)

    return render_template(
        'admin/dashboard.html',
        stats=stats,
        pending_items=pending_items,
        type_breakdown=type_breakdown,
        dept_breakdown=dept_breakdown,
        recent_logs=recent_logs,
        format_file_size=format_file_size
    )

@admin_bp.route('/pending')
@admin_required
def pending_queue():
    items = query_db("""
        SELECT r.*, d.name as department_name, d.code as department_code, s.name as subject_name,
               u.full_name as uploader_name, u.username as uploader_username, u.email as uploader_email, u.role as uploader_role
        FROM resources r
        JOIN departments d ON r.department_id = d.id
        JOIN subjects s ON r.subject_id = s.id
        LEFT JOIN users u ON r.uploader_id = u.id
        WHERE r.status = 'pending'
        ORDER BY r.created_at ASC
    """)
    return render_template('admin/pending.html', items=items, format_file_size=format_file_size)

@admin_bp.route('/approve/<int:resource_id>', methods=['POST'])
@admin_required
def approve_resource(resource_id):
    res = query_db("SELECT * FROM resources WHERE id = ?", (resource_id,), one=True)
    if not res:
        flash('Resource not found.', 'danger')
        return redirect(url_for('admin.pending_queue'))

    execute_db("UPDATE resources SET status = 'approved', rejection_reason = NULL, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (resource_id,))
    log_activity(session['user_id'], 'APPROVE_RESOURCE', f"Approved resource '{res['title']}' (ID: {resource_id})")
    flash(f"Resource '{res['title']}' has been approved and published to the portal.", 'success')
    return redirect(request.referrer or url_for('admin.pending_queue'))

@admin_bp.route('/reject/<int:resource_id>', methods=['POST'])
@admin_required
def reject_resource(resource_id):
    res = query_db("SELECT * FROM resources WHERE id = ?", (resource_id,), one=True)
    if not res:
        flash('Resource not found.', 'danger')
        return redirect(url_for('admin.pending_queue'))

    reason = request.form.get('reason', 'Content does not meet academic quality guidelines or policy.').strip()
    execute_db("UPDATE resources SET status = 'rejected', rejection_reason = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (reason, resource_id))
    log_activity(session['user_id'], 'REJECT_RESOURCE', f"Rejected resource '{res['title']}' (Reason: {reason})")
    flash(f"Resource '{res['title']}' marked as rejected with feedback.", 'warning')
    return redirect(request.referrer or url_for('admin.pending_queue'))

@admin_bp.route('/resources')
@admin_required
def manage_resources():
    q = request.args.get('q', '').strip()
    status_filter = request.args.get('status', '')
    dept_filter = request.args.get('dept', '')

    query_conditions = ["1=1"]
    params = []

    if q:
        query_conditions.append("(r.title LIKE ? OR s.name LIKE ?)")
        params.extend([f"%{q}%", f"%{q}%"])

    if status_filter:
        query_conditions.append("r.status = ?")
        params.append(status_filter)

    if dept_filter and dept_filter.isdigit():
        query_conditions.append("r.department_id = ?")
        params.append(int(dept_filter))

    where_clause = " WHERE " + " AND ".join(query_conditions)

    resources = query_db(f"""
        SELECT r.*, d.code as department_code, s.name as subject_name, u.full_name as uploader_name
        FROM resources r
        JOIN departments d ON r.department_id = d.id
        JOIN subjects s ON r.subject_id = s.id
        LEFT JOIN users u ON r.uploader_id = u.id
        {where_clause}
        ORDER BY r.created_at DESC
    """, params)

    departments = query_db("SELECT * FROM departments WHERE is_active = 1 ORDER BY name ASC")

    return render_template(
        'admin/resources.html',
        resources=resources,
        departments=departments,
        q=q,
        status_filter=status_filter,
        dept_filter=dept_filter,
        format_file_size=format_file_size
    )

@admin_bp.route('/resource/toggle-featured/<int:resource_id>', methods=['POST'])
@admin_required
def toggle_featured(resource_id):
    res = query_db("SELECT is_featured, title FROM resources WHERE id = ?", (resource_id,), one=True)
    if not res:
        flash('Resource not found.', 'danger')
        return redirect(url_for('admin.manage_resources'))

    new_val = 0 if res['is_featured'] else 1
    execute_db("UPDATE resources SET is_featured = ? WHERE id = ?", (new_val, resource_id))
    state_str = "featured" if new_val else "unfeatured"
    log_activity(session['user_id'], 'TOGGLE_FEATURED', f"Marked '{res['title']}' as {state_str}")
    flash(f"Resource '{res['title']}' is now {state_str}.", 'success')
    return redirect(request.referrer or url_for('admin.manage_resources'))

@admin_bp.route('/resource/delete/<int:resource_id>', methods=['POST'])
@admin_required
def delete_resource(resource_id):
    res = query_db("SELECT * FROM resources WHERE id = ?", (resource_id,), one=True)
    if not res:
        flash('Resource not found.', 'danger')
        return redirect(url_for('admin.manage_resources'))

    # Delete physical file
    filepath = os.path.join(Config.UPLOAD_FOLDER, res['file_name'])
    if os.path.isfile(filepath):
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Error removing file: {e}")

    execute_db("DELETE FROM resources WHERE id = ?", (resource_id,))
    log_activity(session['user_id'], 'ADMIN_DELETE_RESOURCE', f"Admin deleted resource '{res['title']}' (ID: {resource_id})")
    flash(f"Resource '{res['title']}' deleted successfully.", 'success')
    return redirect(request.referrer or url_for('admin.manage_resources'))

@admin_bp.route('/users')
@admin_required
def manage_users():
    users = query_db("""
        SELECT u.*, d.name as department_name, d.code as department_code,
               (SELECT COUNT(*) FROM resources WHERE uploader_id = u.id) as upload_count
        FROM users u
        LEFT JOIN departments d ON u.department_id = d.id
        ORDER BY u.created_at DESC
    """)
    departments = query_db("SELECT * FROM departments WHERE is_active = 1 ORDER BY name ASC")
    return render_template('admin/users.html', users=users, departments=departments)

@admin_bp.route('/user/update-role/<int:user_id>', methods=['POST'])
@admin_required
def update_user_role(user_id):
    if user_id == session['user_id']:
        flash('You cannot change your own administrative role.', 'danger')
        return redirect(url_for('admin.manage_users'))

    new_role = request.form.get('role')
    if new_role not in ('student', 'faculty', 'admin'):
        flash('Invalid role specified.', 'warning')
        return redirect(url_for('admin.manage_users'))

    execute_db("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    log_activity(session['user_id'], 'UPDATE_USER_ROLE', f"Changed user ID {user_id} role to {new_role}")
    flash('User role updated successfully.', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/user/toggle-active/<int:user_id>', methods=['POST'])
@admin_required
def toggle_user_active(user_id):
    if user_id == session['user_id']:
        flash('You cannot deactivate your own administrative account.', 'danger')
        return redirect(url_for('admin.manage_users'))

    user = query_db("SELECT is_active, username FROM users WHERE id = ?", (user_id,), one=True)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin.manage_users'))

    new_state = 0 if user['is_active'] else 1
    execute_db("UPDATE users SET is_active = ? WHERE id = ?", (new_state, user_id))
    action_text = "activated" if new_state else "deactivated"
    log_activity(session['user_id'], 'TOGGLE_USER_STATUS', f"User {user['username']} {action_text}")
    flash(f"User account '{user['username']}' has been {action_text}.", 'info')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/departments', methods=['GET', 'POST'])
@admin_required
def manage_departments():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        code = request.form.get('code', '').strip().upper()
        description = request.form.get('description', '').strip()
        icon = request.form.get('icon', 'fas fa-graduation-cap').strip()

        if not name or not code:
            flash('Department Name and Department Code are required.', 'warning')
        else:
            try:
                execute_db(
                    "INSERT INTO departments (name, code, description, icon) VALUES (?, ?, ?, ?)",
                    (name, code, description, icon)
                )
                log_activity(session['user_id'], 'ADD_DEPARTMENT', f"Created department '{code} - {name}'")
                flash(f"Department '{code}' created successfully!", 'success')
            except Exception as e:
                flash(f"Error adding department (possibly duplicate code or name): {e}", 'danger')
        return redirect(url_for('admin.manage_departments'))

    departments = query_db("""
        SELECT d.*, 
               (SELECT COUNT(*) FROM subjects WHERE department_id = d.id) as subject_count,
               (SELECT COUNT(*) FROM resources WHERE department_id = d.id) as resource_count
        FROM departments d
        ORDER BY d.name ASC
    """)
    return render_template('admin/departments.html', departments=departments)

@admin_bp.route('/subjects', methods=['GET', 'POST'])
@admin_required
def manage_subjects():
    dept_id = request.args.get('dept')

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        code = request.form.get('code', '').strip().upper()
        department_id = request.form.get('department_id')
        semester = request.form.get('semester')
        description = request.form.get('description', '').strip()

        if not name or not code or not department_id or not semester:
            flash('All subject fields must be filled.', 'warning')
        else:
            try:
                execute_db(
                    "INSERT INTO subjects (name, code, department_id, semester, description) VALUES (?, ?, ?, ?, ?)",
                    (name, code, int(department_id), int(semester), description)
                )
                log_activity(session['user_id'], 'ADD_SUBJECT', f"Created subject '{code} - {name}'")
                flash(f"Subject '{code}' added successfully!", 'success')
            except Exception as e:
                flash(f"Error adding subject (possibly duplicate code): {e}", 'danger')
        return redirect(url_for('admin.manage_subjects', dept=department_id))

    departments = query_db("SELECT * FROM departments WHERE is_active = 1 ORDER BY name ASC")
    
    if dept_id and dept_id.isdigit():
        subjects = query_db("""
            SELECT s.*, d.name as department_name, d.code as department_code,
                   (SELECT COUNT(*) FROM resources WHERE subject_id = s.id) as resource_count
            FROM subjects s
            JOIN departments d ON s.department_id = d.id
            WHERE s.department_id = ?
            ORDER BY s.semester, s.name
        """, (int(dept_id),))
    else:
        subjects = query_db("""
            SELECT s.*, d.name as department_name, d.code as department_code,
                   (SELECT COUNT(*) FROM resources WHERE subject_id = s.id) as resource_count
            FROM subjects s
            JOIN departments d ON s.department_id = d.id
            ORDER BY d.name, s.semester, s.name
        """)

    return render_template('admin/subjects.html', subjects=subjects, departments=departments, selected_dept=dept_id)

@admin_bp.route('/logs')
@admin_required
def activity_logs():
    logs = query_db("""
        SELECT l.*, u.username, u.full_name, u.role
        FROM activity_logs l
        LEFT JOIN users u ON l.user_id = u.id
        ORDER BY l.created_at DESC
        LIMIT 100
    """)
    return render_template('admin/logs.html', logs=logs)
