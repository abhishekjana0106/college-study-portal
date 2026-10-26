import sqlite3
import os
from flask import g, current_app
from config import Config

def get_db():
    """Get database connection for current request context."""
    if 'db' not in g:
        g.db = sqlite3.connect(Config.DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON;")
        g.db.execute("PRAGMA journal_mode = WAL;")
    return g.db

def close_db(e=None):
    """Close database connection at end of request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    """Execute a query and fetch results."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=(), commit=True):
    """Execute an INSERT/UPDATE/DELETE query and return the lastrowid or rowcount."""
    db = get_db()
    cur = db.execute(query, args)
    if commit:
        db.commit()
    last_id = cur.lastrowid
    cur.close()
    return last_id

def init_db():
    """Create database tables and indexes if they do not exist."""
    os.makedirs(os.path.dirname(Config.DATABASE), exist_ok=True)
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    
    conn = sqlite3.connect(Config.DATABASE)
    conn.execute("PRAGMA foreign_keys = ON;")
    cur = conn.cursor()

    # 1. Departments Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            code TEXT NOT NULL UNIQUE,
            description TEXT,
            icon TEXT DEFAULT 'fas fa-graduation-cap',
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    # 2. Subjects Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT NOT NULL,
            department_id INTEGER NOT NULL,
            semester INTEGER NOT NULL,
            description TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE,
            UNIQUE(code, department_id)
        );
    ''')

    # 3. Users Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            roll_number TEXT,
            department_id INTEGER,
            semester INTEGER,
            role TEXT DEFAULT 'student', -- 'student', 'faculty', 'admin'
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
        );
    ''')

    # 4. Resources Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            resource_type TEXT NOT NULL, -- 'Question Paper', 'Lecture Notes', 'Syllabus', 'Lab Manual', 'Assignment', 'Reference Book'
            department_id INTEGER NOT NULL,
            semester INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            academic_year TEXT DEFAULT '2025-2026',
            exam_type TEXT DEFAULT 'End-Semester', -- 'Mid-Term 1', 'Mid-Term 2', 'End-Semester', 'Model Exam', 'Supplementary', 'N/A'
            file_name TEXT NOT NULL,
            original_file_name TEXT NOT NULL,
            file_size INTEGER DEFAULT 0, -- in bytes
            file_ext TEXT NOT NULL,
            uploader_id INTEGER,
            status TEXT DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
            rejection_reason TEXT,
            download_count INTEGER DEFAULT 0,
            view_count INTEGER DEFAULT 0,
            is_featured INTEGER DEFAULT 0,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE,
            FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
            FOREIGN KEY (uploader_id) REFERENCES users(id) ON DELETE SET NULL
        );
    ''')

    # 5. Resource Ratings & Reviews Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS resource_ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            review TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (resource_id) REFERENCES resources(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(resource_id, user_id)
        );
    ''')

    # 6. Bookmarks Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (resource_id) REFERENCES resources(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(resource_id, user_id)
        );
    ''')

    # 7. Activity Logs Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            details TEXT,
            ip_address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        );
    ''')

    # Performance Indexes
    cur.execute('CREATE INDEX IF NOT EXISTS idx_resources_dept ON resources(department_id);')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_resources_subj ON resources(subject_id);')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_resources_sem ON resources(semester);')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_resources_type ON resources(resource_type);')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_resources_status ON resources(status);')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_resources_created ON resources(created_at DESC);')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_subjects_dept_sem ON subjects(department_id, semester);')

    conn.commit()
    conn.close()
    print("Database schema successfully initialized.")
