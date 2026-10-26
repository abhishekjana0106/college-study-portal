from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import query_db, execute_db
from helpers import login_required, log_activity, get_current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '')

        if not identifier or not password:
            flash('Please enter both username/email and password.', 'warning')
            return render_template('auth/login.html')

        user = query_db(
            "SELECT * FROM users WHERE (username = ? OR email = ?)",
            (identifier, identifier),
            one=True
        )

        if not user or not check_password_hash(user['password_hash'], password):
            flash('Invalid username/email or password.', 'danger')
            return render_template('auth/login.html')

        if not user['is_active']:
            flash('Your account has been deactivated. Please contact the administrator.', 'danger')
            return render_template('auth/login.html')

        # Set session
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['full_name'] = user['full_name']
        session['role'] = user['role']
        session['department_id'] = user['department_id']

        log_activity(user['id'], 'LOGIN', f"User {user['username']} logged in successfully")

        flash(f"Welcome back, {user['full_name']}!", 'success')
        next_page = request.args.get('next')
        if next_page and next_page.startswith('/'):
            return redirect(next_page)
        return redirect(url_for('main.index'))

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('main.index'))

    departments = query_db("SELECT * FROM departments WHERE is_active = 1 ORDER BY name ASC")

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        username = request.form.get('username', '').strip().lower()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        roll_number = request.form.get('roll_number', '').strip().upper()
        department_id = request.form.get('department_id')
        semester = request.form.get('semester')
        role = request.form.get('role', 'student')

        # Validation
        if not full_name or not username or not email or not password:
            flash('All required fields must be filled.', 'warning')
            return render_template('auth/register.html', departments=departments)

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html', departments=departments)

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'warning')
            return render_template('auth/register.html', departments=departments)

        # Check existing
        existing_user = query_db(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            (username, email),
            one=True
        )
        if existing_user:
            if existing_user['username'] == username:
                flash('Username is already taken. Please choose another.', 'warning')
            else:
                flash('Email is already registered. Please log in.', 'warning')
            return render_template('auth/register.html', departments=departments)

        # Allow student or faculty registration (faculty requires admin verification or defaults to student/faculty)
        assigned_role = 'faculty' if role == 'faculty' else 'student'

        pwd_hash = generate_password_hash(password)
        user_id = execute_db(
            """INSERT INTO users (username, email, password_hash, full_name, roll_number, department_id, semester, role)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (username, email, pwd_hash, full_name, roll_number or None, department_id or None, semester or None, assigned_role)
        )

        log_activity(user_id, 'REGISTER', f"New account registered: {username} ({assigned_role})")

        # Auto login
        session['user_id'] = user_id
        session['username'] = username
        session['full_name'] = full_name
        session['role'] = assigned_role
        session['department_id'] = department_id

        flash('Registration successful! Welcome to the Centralized College Portal.', 'success')
        return redirect(url_for('main.index'))

    return render_template('auth/register.html', departments=departments)

@auth_bp.route('/logout')
def logout():
    user_id = session.get('user_id')
    if user_id:
        log_activity(user_id, 'LOGOUT', "User logged out")
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = get_current_user()
    departments = query_db("SELECT * FROM departments WHERE is_active = 1 ORDER BY name ASC")

    # Fetch user statistics
    stats = {
        'uploads_count': query_db("SELECT COUNT(*) as cnt FROM resources WHERE uploader_id = ?", (user['id'],), one=True)['cnt'],
        'approved_count': query_db("SELECT COUNT(*) as cnt FROM resources WHERE uploader_id = ? AND status = 'approved'", (user['id'],), one=True)['cnt'],
        'pending_count': query_db("SELECT COUNT(*) as cnt FROM resources WHERE uploader_id = ? AND status = 'pending'", (user['id'],), one=True)['cnt'],
        'bookmarks_count': query_db("SELECT COUNT(*) as cnt FROM bookmarks WHERE user_id = ?", (user['id'],), one=True)['cnt'],
        'total_downloads': query_db("SELECT COALESCE(SUM(download_count), 0) as cnt FROM resources WHERE uploader_id = ?", (user['id'],), one=True)['cnt']
    }

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update_info':
            full_name = request.form.get('full_name', '').strip()
            email = request.form.get('email', '').strip().lower()
            roll_number = request.form.get('roll_number', '').strip().upper()
            department_id = request.form.get('department_id')
            semester = request.form.get('semester')

            if not full_name or not email:
                flash('Full Name and Email are required.', 'warning')
                return render_template('auth/profile.html', user=user, stats=stats, departments=departments)

            # Check email collision
            existing = query_db("SELECT id FROM users WHERE email = ? AND id != ?", (email, user['id']), one=True)
            if existing:
                flash('This email is already associated with another account.', 'danger')
                return render_template('auth/profile.html', user=user, stats=stats, departments=departments)

            execute_db(
                """UPDATE users SET full_name = ?, email = ?, roll_number = ?, department_id = ?, semester = ?
                   WHERE id = ?""",
                (full_name, email, roll_number or None, department_id or None, semester or None, user['id'])
            )
            session['full_name'] = full_name
            session['department_id'] = department_id
            log_activity(user['id'], 'UPDATE_PROFILE', "Profile details updated")
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('auth.profile'))

        elif action == 'change_password':
            current_password = request.form.get('current_password', '')
            new_password = request.form.get('new_password', '')
            confirm_new_password = request.form.get('confirm_new_password', '')

            if not check_password_hash(user['password_hash'], current_password):
                flash('Current password entered is incorrect.', 'danger')
                return render_template('auth/profile.html', user=user, stats=stats, departments=departments)

            if len(new_password) < 6:
                flash('New password must be at least 6 characters long.', 'warning')
                return render_template('auth/profile.html', user=user, stats=stats, departments=departments)

            if new_password != confirm_new_password:
                flash('New passwords do not match.', 'danger')
                return render_template('auth/profile.html', user=user, stats=stats, departments=departments)

            new_hash = generate_password_hash(new_password)
            execute_db("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user['id']))
            log_activity(user['id'], 'CHANGE_PASSWORD', "Password changed successfully")
            flash('Password updated successfully!', 'success')
            return redirect(url_for('auth.profile'))

    return render_template('auth/profile.html', user=user, stats=stats, departments=departments)
