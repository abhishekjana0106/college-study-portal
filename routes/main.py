import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_from_directory, jsonify, abort
from config import Config
from database import query_db, execute_db
from helpers import get_current_user, login_required, log_activity, format_file_size

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Metrics
    stats = {
        'total_resources': query_db("SELECT COUNT(*) as c FROM resources WHERE status = 'approved'", one=True)['c'],
        'total_downloads': query_db("SELECT COALESCE(SUM(download_count), 0) as c FROM resources WHERE status = 'approved'", one=True)['c'],
        'total_departments': query_db("SELECT COUNT(*) as c FROM departments WHERE is_active = 1", one=True)['c'],
        'total_users': query_db("SELECT COUNT(*) as c FROM users WHERE is_active = 1", one=True)['c']
    }

    # Featured Resources
    featured = query_db("""
        SELECT r.*, d.name as department_name, d.code as department_code, s.name as subject_name,
               COALESCE((SELECT AVG(rating) FROM resource_ratings WHERE resource_id = r.id), 0) as avg_rating,
               (SELECT COUNT(*) FROM resource_ratings WHERE resource_id = r.id) as rating_count
        FROM resources r
        JOIN departments d ON r.department_id = d.id
        JOIN subjects s ON r.subject_id = s.id
        WHERE r.status = 'approved' AND r.is_featured = 1
        ORDER BY r.download_count DESC, r.created_at DESC
        LIMIT 6
    """)

    # Recent Uploads
    recent = query_db("""
        SELECT r.*, d.name as department_name, d.code as department_code, s.name as subject_name,
               COALESCE((SELECT AVG(rating) FROM resource_ratings WHERE resource_id = r.id), 0) as avg_rating
        FROM resources r
        JOIN departments d ON r.department_id = d.id
        JOIN subjects s ON r.subject_id = s.id
        WHERE r.status = 'approved'
        ORDER BY r.created_at DESC
        LIMIT 6
    """)

    # Departments with resource counts
    departments = query_db("""
        SELECT d.*, 
               (SELECT COUNT(*) FROM resources r WHERE r.department_id = d.id AND r.status = 'approved') as resource_count
        FROM departments d
        WHERE d.is_active = 1
        ORDER BY d.name ASC
    """)

    # Top Question Papers
    question_papers = query_db("""
        SELECT r.*, d.code as department_code, s.name as subject_name
        FROM resources r
        JOIN departments d ON r.department_id = d.id
        JOIN subjects s ON r.subject_id = s.id
        WHERE r.status = 'approved' AND r.resource_type = 'Question Paper'
        ORDER BY r.download_count DESC, r.created_at DESC
        LIMIT 4
    """)

    return render_template(
        'index.html',
        stats=stats,
        featured=featured,
        recent=recent,
        departments=departments,
        question_papers=question_papers,
        format_file_size=format_file_size
    )

@main_bp.route('/browse')
def browse():
    q = request.args.get('q', '').strip()
    dept_id = request.args.get('dept', '')
    sem = request.args.get('sem', '')
    subj_id = request.args.get('subj', '')
    res_type = request.args.get('type', '')
    year = request.args.get('year', '')
    exam = request.args.get('exam', '')
    sort_by = request.args.get('sort', 'newest')
    page = int(request.args.get('page', 1))
    per_page = 12
    offset = (page - 1) * per_page

    query_conditions = ["r.status = 'approved'"]
    params = []

    if q:
        query_conditions.append("(r.title LIKE ? OR r.description LIKE ? OR r.tags LIKE ? OR s.name LIKE ?)")
        search_term = f"%{q}%"
        params.extend([search_term, search_term, search_term, search_term])

    if dept_id and dept_id.isdigit():
        query_conditions.append("r.department_id = ?")
        params.append(int(dept_id))

    if sem and sem.isdigit():
        query_conditions.append("r.semester = ?")
        params.append(int(sem))

    if subj_id and subj_id.isdigit():
        query_conditions.append("r.subject_id = ?")
        params.append(int(subj_id))

    if res_type:
        query_conditions.append("r.resource_type = ?")
        params.append(res_type)

    if year:
        query_conditions.append("r.academic_year = ?")
        params.append(year)

    if exam:
        query_conditions.append("r.exam_type = ?")
        params.append(exam)

    where_clause = " WHERE " + " AND ".join(query_conditions)

    # Sorting
    if sort_by == 'downloads':
        order_clause = "ORDER BY r.download_count DESC, r.created_at DESC"
    elif sort_by == 'rating':
        order_clause = "ORDER BY avg_rating DESC, r.download_count DESC"
    elif sort_by == 'title':
        order_clause = "ORDER BY r.title ASC"
    else:
        order_clause = "ORDER BY r.created_at DESC"

    # Count total matching
    count_sql = f"""
        SELECT COUNT(*) as total
        FROM resources r
        JOIN departments d ON r.department_id = d.id
        JOIN subjects s ON r.subject_id = s.id
        {where_clause}
    """
    total_resources = query_db(count_sql, params, one=True)['total']
    total_pages = max(1, (total_resources + per_page - 1) // per_page)

    # Select resources
    select_sql = f"""
        SELECT r.*, d.name as department_name, d.code as department_code, s.name as subject_name, s.code as subject_code,
               u.full_name as uploader_name, u.role as uploader_role,
               COALESCE((SELECT AVG(rating) FROM resource_ratings WHERE resource_id = r.id), 0) as avg_rating,
               (SELECT COUNT(*) FROM resource_ratings WHERE resource_id = r.id) as rating_count
        FROM resources r
        JOIN departments d ON r.department_id = d.id
        JOIN subjects s ON r.subject_id = s.id
        LEFT JOIN users u ON r.uploader_id = u.id
        {where_clause}
        {order_clause}
        LIMIT ? OFFSET ?
    """
    query_params = list(params) + [per_page, offset]
    resources = query_db(select_sql, query_params)

    # Master dropdown options
    departments = query_db("SELECT * FROM departments WHERE is_active = 1 ORDER BY name ASC")
    
    # If a department is selected, filter subjects list accordingly
    if dept_id and dept_id.isdigit():
        subjects = query_db("SELECT * FROM subjects WHERE department_id = ? AND is_active = 1 ORDER BY semester, name", (dept_id,))
    else:
        subjects = query_db("SELECT * FROM subjects WHERE is_active = 1 ORDER BY name ASC")

    # Distinct academic years available
    available_years = [r['academic_year'] for r in query_db("SELECT DISTINCT academic_year FROM resources WHERE status = 'approved' ORDER BY academic_year DESC")]
    if not available_years:
        available_years = ['2025-2026', '2024-2025', '2023-2024', '2022-2023']

    return render_template(
        'browse.html',
        resources=resources,
        total_resources=total_resources,
        departments=departments,
        subjects=subjects,
        available_years=available_years,
        page=page,
        total_pages=total_pages,
        q=q,
        selected_dept=dept_id,
        selected_sem=sem,
        selected_subj=subj_id,
        selected_type=res_type,
        selected_year=year,
        selected_exam=exam,
        selected_sort=sort_by,
        format_file_size=format_file_size
    )

@main_bp.route('/resource/<int:resource_id>')
def resource_detail(resource_id):
    resource = query_db("""
        SELECT r.*, d.name as department_name, d.code as department_code, 
               s.name as subject_name, s.code as subject_code,
               u.full_name as uploader_name, u.role as uploader_role, u.username as uploader_username,
               COALESCE((SELECT AVG(rating) FROM resource_ratings WHERE resource_id = r.id), 0) as avg_rating,
               (SELECT COUNT(*) FROM resource_ratings WHERE resource_id = r.id) as rating_count
        FROM resources r
        JOIN departments d ON r.department_id = d.id
        JOIN subjects s ON r.subject_id = s.id
        LEFT JOIN users u ON r.uploader_id = u.id
        WHERE r.id = ?
    """, (resource_id,), one=True)

    if not resource:
        flash('Requested resource not found.', 'danger')
        return redirect(url_for('main.browse'))

    # If pending or rejected, only uploader or admin can view
    if resource['status'] != 'approved':
        current_uid = session.get('user_id')
        current_role = session.get('role')
        if current_role != 'admin' and current_uid != resource['uploader_id']:
            flash('This resource is currently under review.', 'warning')
            return redirect(url_for('main.browse'))

    # Increment view count
    execute_db("UPDATE resources SET view_count = view_count + 1 WHERE id = ?", (resource_id,))

    # Check bookmark status for current user
    user_id = session.get('user_id')
    is_bookmarked = False
    user_rating = None
    if user_id:
        bm = query_db("SELECT id FROM bookmarks WHERE resource_id = ? AND user_id = ?", (resource_id, user_id), one=True)
        is_bookmarked = (bm is not None)
        ur = query_db("SELECT rating, review FROM resource_ratings WHERE resource_id = ? AND user_id = ?", (resource_id, user_id), one=True)
        if ur:
            user_rating = ur

    # Fetch reviews
    reviews = query_db("""
        SELECT rr.*, u.full_name, u.username, u.role
        FROM resource_ratings rr
        JOIN users u ON rr.user_id = u.id
        WHERE rr.resource_id = ?
        ORDER BY rr.created_at DESC
    """, (resource_id,))

    # Related resources
    related = query_db("""
        SELECT r.*, d.code as department_code, s.name as subject_name,
               COALESCE((SELECT AVG(rating) FROM resource_ratings WHERE resource_id = r.id), 0) as avg_rating
        FROM resources r
        JOIN departments d ON r.department_id = d.id
        JOIN subjects s ON r.subject_id = s.id
        WHERE r.id != ? AND r.status = 'approved' AND (r.subject_id = ? OR r.department_id = ?)
        ORDER BY r.download_count DESC
        LIMIT 4
    """, (resource_id, resource['subject_id'], resource['department_id']))

    # Split tags
    tag_list = [t.strip() for t in resource['tags'].split(',')] if resource['tags'] else []

    return render_template(
        'resource_detail.html',
        resource=resource,
        is_bookmarked=is_bookmarked,
        user_rating=user_rating,
        reviews=reviews,
        related=related,
        tag_list=tag_list,
        format_file_size=format_file_size
    )

@main_bp.route('/download/<int:resource_id>')
def download_resource(resource_id):
    resource = query_db("SELECT * FROM resources WHERE id = ?", (resource_id,), one=True)
    if not resource:
        flash('Resource not found.', 'danger')
        return redirect(url_for('main.browse'))

    filepath = os.path.join(Config.UPLOAD_FOLDER, resource['file_name'])
    if not os.path.isfile(filepath):
        flash('File not found on server.', 'danger')
        return redirect(url_for('main.resource_detail', resource_id=resource_id))

    # Increment download count
    execute_db("UPDATE resources SET download_count = download_count + 1 WHERE id = ?", (resource_id,))
    
    user_id = session.get('user_id')
    if user_id:
        log_activity(user_id, 'DOWNLOAD', f"Downloaded resource: {resource['title']} (ID: {resource['id']})")

    return send_from_directory(
        Config.UPLOAD_FOLDER,
        resource['file_name'],
        as_attachment=True,
        download_name=resource['original_file_name']
    )

@main_bp.route('/preview/<int:resource_id>')
def preview_resource(resource_id):
    resource = query_db("SELECT * FROM resources WHERE id = ?", (resource_id,), one=True)
    if not resource:
        abort(404)

    filepath = os.path.join(Config.UPLOAD_FOLDER, resource['file_name'])
    if not os.path.isfile(filepath):
        abort(404)

    return send_from_directory(
        Config.UPLOAD_FOLDER,
        resource['file_name'],
        as_attachment=False
    )

@main_bp.route('/bookmark/<int:resource_id>', methods=['POST'])
@login_required
def toggle_bookmark(resource_id):
    user_id = session['user_id']
    existing = query_db("SELECT id FROM bookmarks WHERE resource_id = ? AND user_id = ?", (resource_id, user_id), one=True)

    if existing:
        execute_db("DELETE FROM bookmarks WHERE id = ?", (existing['id'],))
        is_bookmarked = False
        message = "Removed from your bookmarks."
    else:
        execute_db("INSERT INTO bookmarks (resource_id, user_id) VALUES (?, ?)", (resource_id, user_id))
        is_bookmarked = True
        message = "Added to your bookmarks."

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
        return jsonify({'status': 'success', 'is_bookmarked': is_bookmarked, 'message': message})

    flash(message, 'info')
    return redirect(request.referrer or url_for('main.resource_detail', resource_id=resource_id))

@main_bp.route('/rate/<int:resource_id>', methods=['POST'])
@login_required
def rate_resource(resource_id):
    user_id = session['user_id']
    rating_val = request.form.get('rating')
    review_text = request.form.get('review', '').strip()

    if not rating_val or not rating_val.isdigit():
        flash('Please select a valid rating between 1 and 5.', 'warning')
        return redirect(url_for('main.resource_detail', resource_id=resource_id))

    rating_int = int(rating_val)
    if rating_int < 1 or rating_int > 5:
        flash('Rating must be between 1 and 5.', 'warning')
        return redirect(url_for('main.resource_detail', resource_id=resource_id))

    execute_db("""
        INSERT INTO resource_ratings (resource_id, user_id, rating, review)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(resource_id, user_id) DO UPDATE SET rating=excluded.rating, review=excluded.review, created_at=CURRENT_TIMESTAMP
    """, (resource_id, user_id, rating_int, review_text))

    log_activity(user_id, 'RATE_RESOURCE', f"Rated resource ID {resource_id} with {rating_int} stars")
    flash('Thank you for rating and reviewing this study material!', 'success')
    return redirect(url_for('main.resource_detail', resource_id=resource_id))

@main_bp.route('/bookmarks')
@login_required
def bookmarks():
    user_id = session['user_id']
    bookmarks_list = query_db("""
        SELECT r.*, d.name as department_name, d.code as department_code, 
               s.name as subject_name, b.created_at as bookmarked_at,
               COALESCE((SELECT AVG(rating) FROM resource_ratings WHERE resource_id = r.id), 0) as avg_rating
        FROM bookmarks b
        JOIN resources r ON b.resource_id = r.id
        JOIN departments d ON r.department_id = d.id
        JOIN subjects s ON r.subject_id = s.id
        WHERE b.user_id = ?
        ORDER BY b.created_at DESC
    """, (user_id,))

    return render_template('bookmarks.html', bookmarks=bookmarks_list, format_file_size=format_file_size)

@main_bp.route('/offline')
def offline():
    return render_template('offline.html')

@main_bp.route('/presentation')
def presentation():
    return render_template('presentation.html')

@main_bp.route('/download-video')
def download_video():
    video_path = os.path.join(Config.BASE_DIR, 'project_presentation_video.mp4')
    if not os.path.isfile(video_path):
        flash('Video file is being generated or was moved.', 'warning')
        return redirect(url_for('main.presentation'))
    return send_from_directory(
        Config.BASE_DIR,
        'project_presentation_video.mp4',
        as_attachment=True,
        download_name='College_Study_Material_Portal_Video_Presentation.mp4'
    )

@main_bp.route('/download-codebook')
def download_codebook_pdf():
    pdf_path = os.path.join(Config.BASE_DIR, 'College_Study_Material_Portal_Complete_Code.pdf')
    if not os.path.isfile(pdf_path):
        flash('Codebook PDF not found.', 'warning')
        return redirect(url_for('main.presentation'))
    return send_from_directory(
        Config.BASE_DIR,
        'College_Study_Material_Portal_Complete_Code.pdf',
        as_attachment=True,
        download_name='College_Study_Material_Portal_Complete_Code.pdf'
    )
