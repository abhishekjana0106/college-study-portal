from flask import Blueprint, request, jsonify
from database import query_db

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/subjects')
def get_subjects():
    dept_id = request.args.get('dept_id')
    semester = request.args.get('semester')

    query_str = "SELECT id, name, code, semester FROM subjects WHERE is_active = 1"
    params = []

    if dept_id and dept_id.isdigit():
        query_str += " AND department_id = ?"
        params.append(int(dept_id))

    if semester and semester.isdigit():
        query_str += " AND semester = ?"
        params.append(int(semester))

    query_str += " ORDER BY semester ASC, name ASC"
    subjects = query_db(query_str, params)

    return jsonify([
        {
            'id': s['id'],
            'name': s['name'],
            'code': s['code'],
            'semester': s['semester']
        } for s in subjects
    ])

@api_bp.route('/quick-search')
def quick_search():
    q = request.args.get('q', '').strip()
    if not q or len(q) < 2:
        return jsonify([])

    search_term = f"%{q}%"
    results = query_db("""
        SELECT r.id, r.title, r.resource_type, r.academic_year, d.code as dept_code, s.name as subject_name
        FROM resources r
        JOIN departments d ON r.department_id = d.id
        JOIN subjects s ON r.subject_id = s.id
        WHERE r.status = 'approved' AND (r.title LIKE ? OR r.tags LIKE ? OR s.name LIKE ?)
        ORDER BY r.download_count DESC
        LIMIT 6
    """, (search_term, search_term, search_term))

    return jsonify([
        {
            'id': r['id'],
            'title': r['title'],
            'type': r['resource_type'],
            'year': r['academic_year'],
            'dept': r['dept_code'],
            'subject': r['subject_name']
        } for r in results
    ])
