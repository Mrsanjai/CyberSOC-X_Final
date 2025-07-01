import json
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp

class User:
    def __init__(self, id, username, password_hash, role, otp_secret):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.otp_secret = otp_secret

    def get_id(self):
        return str(self.id)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_totp_uri(self):
        return f"otpauth://totp/CyberSOC-X:{self.username}?secret={self.otp_secret}&issuer=CyberSOC-X"

    def verify_totp(self, token):
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(token)

    # ✅ Flask-Login required properties
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __init__(self, id, username, password_hash, role, otp_secret):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.otp_secret = otp_secret

    def get_id(self):
        return str(self.id)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_totp_uri(self):
        return f"otpauth://totp/CyberSOC-X:{self.username}?secret={self.otp_secret}&issuer=CyberSOC-X"

    def verify_totp(self, token):
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(token)

def load_user(user_id):
    with open("users.json", "r") as f:
        users = json.load(f)
    for u in users.values():
        if str(u["id"]) == str(user_id):
            return User(u["id"], u["username"], u["password_hash"], u["role"], u["otp_secret"])
    return None

def save_user(username, password, role="analyst"):
    with open("users.json", "r+") as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            users = {}
        uid = str(len(users) + 1)
        otp_secret = pyotp.random_base32()
        users[uid] = {
            "id": uid,
            "username": username,
            "password_hash": generate_password_hash(password),
            "role": role,
            "otp_secret": otp_secret
        }
        f.seek(0)
        json.dump(users, f, indent=4)
        f.truncate()
    return True
