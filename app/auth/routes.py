from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_user, logout_user, login_required
from app.auth.utils import save_user, load_user, User
from app.windows_log_reader import get_windows_logs
import json, pyotp, qrcode, io, base64

# --- Auth Blueprint ---
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role", "analyst")
        save_user(username, password, role)

        with open("users.json", "r") as f:
            users = json.load(f)
        u = next((u for u in users.values() if u["username"] == username), None)

        if u:
            user = User(u["id"], u["username"], u["password_hash"], u["role"], u["otp_secret"])
            otp_uri = user.get_totp_uri()
            current_otp = pyotp.TOTP(user.otp_secret).now()
            print("\n📲 TOTP URI:", otp_uri)
            print("🔐 Current OTP:", current_otp)

            img = qrcode.make(otp_uri)
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            qr_b64 = base64.b64encode(buf.getvalue()).decode()

            return render_template("show_qr.html", username=username, otp_uri=otp_uri, qr_b64=qr_b64)
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with open("users.json", "r") as f:
            users = json.load(f)

        for u in users.values():
            if u["username"] == username:
                user = User(u["id"], u["username"], u["password_hash"], u["role"], u["otp_secret"])
                if user.verify_password(password):
                    session["temp_user_id"] = user.id
                    return redirect(url_for("auth.mfa"))
                else:
                    flash("Invalid password", "danger")
                    return redirect(url_for("auth.login"))

        flash("User not found", "danger")
    return render_template("login.html")

@auth_bp.route("/mfa", methods=["GET", "POST"])
def mfa():
    if request.method == "POST":
        token = request.form["token"]
        user = load_user(session.get("temp_user_id"))

        if user and user.verify_totp(token):
            login_user(user)
            session.pop("temp_user_id", None)
            flash("Login successful", "success")
            return redirect(url_for("dashboard.dashboard"))
        else:
            flash("Invalid token", "danger")
    return render_template("mfa.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))

from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def dashboard():
    # Pass user to template
    return render_template('dashboard.html', user=current_user)
