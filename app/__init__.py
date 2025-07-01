from flask import Flask
from flask_login import LoginManager
from app.auth.utils import load_user

# Dummy monitor start functions
from app.log_monitor import start_monitoring
from app.real_log_monitor import start_real_log_monitor

start_monitoring()
start_real_log_monitor()

def create_app():
    app = Flask(__name__)
    app.secret_key = "super_secure_secret_key"

    # --- Login Manager ---
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(user_id):
        return load_user(user_id)

    # --- Blueprints ---
    from app.auth.routes import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.system_monitor import monitor_bp as system_monitor_bp    # ✅ Handles /monitor and /monitor/data
    from app.routes.monitor import monitor_bp as winlog_bp                   # ✅ Handles /win-monitor
    from app.routes.alert_viewer import alerts_bp
    from app.routes.sysmon_upload import sysmon_bp
    from app.routes.pcap_upload import pcap_bp
    from app.routes.training_lab import training_bp
    from app.routes.ir_console import ir_bp

    # --- Register Blueprints ---
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(system_monitor_bp)       # /monitor and /monitor/data
    app.register_blueprint(winlog_bp, url_prefix="/windows-logs")         # /win-monitor
    app.register_blueprint(alerts_bp)
    app.register_blueprint(sysmon_bp)
    app.register_blueprint(pcap_bp)
    app.register_blueprint(training_bp)
    app.register_blueprint(ir_bp)

    return app
