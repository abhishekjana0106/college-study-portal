import os
import socket
from flask import Flask, render_template
from config import Config
from database import close_db, init_db, query_db
from helpers import get_current_user

def get_lan_ip():
    """Discover host's local IPv4 address for local network access."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        # Doesn't need to actually send packets, just determines the outbound interface
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return '127.0.0.1'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database if not already existing
    if not os.path.exists(Config.DATABASE):
        with app.app_context():
            from seed_data import seed_database
            seed_database()

    # Register Database teardown
    app.teardown_appcontext(close_db)

    # Custom Jinja filters
    @app.template_filter('str_date')
    def filter_str_date(val):
        if not val:
            return ""
        if hasattr(val, 'strftime'):
            return val.strftime('%Y-%m-%d')
        return str(val)[:10]

    @app.template_filter('str_time')
    def filter_str_time(val):
        if not val:
            return ""
        if hasattr(val, 'strftime'):
            return val.strftime('%Y-%m-%d %H:%M')
        return str(val)[:19]

    # Context processors
    lan_ip = get_lan_ip()

    @app.context_processor
    def inject_global_data():
        user = get_current_user()
        pending_count = 0
        if user and user['role'] == 'admin':
            res = query_db("SELECT COUNT(*) as c FROM resources WHERE status = 'pending'", one=True)
            pending_count = res['c'] if res else 0

        return {
            'current_user': user,
            'pending_review_count': pending_count,
            'lan_ip': lan_ip,
            'server_port': Config.PORT
        }

    # Register Blueprints
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.upload import upload_bp
    from routes.admin import admin_bp
    from routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', error_code=404, message="The page or study material you requested was not found."), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error.html', error_code=500, message="An internal server error occurred. Please try again shortly."), 500

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return render_template('error.html', error_code=413, message="The uploaded file exceeds the 64 MB size limit. Please upload a smaller file or compressed archive."), 413

    return app

if __name__ == '__main__':
    application = create_app()
    lan_ip = get_lan_ip()
    port = Config.PORT

    print("\n" + "=" * 68)
    print("  CENTRALIZED COLLEGE STUDY MATERIAL & QUESTION PAPER PORTAL")
    print("=" * 68)
    print(f"  * Local Access:     http://localhost:{port}")
    print(f"  * LAN/Offline WiFi: http://{lan_ip}:{port}")
    print("  * Status:           Online & Local Network Ready")
    print("--------------------------------------------------------------------")
    print("  Default Credentials:")
    print("    - Admin:   username: admin       | password: admin123")
    print("    - Faculty: username: prof_sharma | password: faculty123")
    print("    - Student: username: student1    | password: student123")
    print("=" * 68 + "\n")

    application.run(host=Config.HOST, port=port, debug=True)
