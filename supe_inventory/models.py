from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime

# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import for Secrets Module (Given by Python)
import secrets

# Imports for Flask_Login
from flask_login import UserMixin, LoginManager

# Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    supe = db.relationship('Supe', backref = 'owner', lazy = True)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User {self.email} has been added to the database"

class Supe(db.Model):
    id = db.Column(db.String, primary_key=True)
    super_hero_name = db.Column(db.String(150))
    secret_identity = db.Column(db.String(150), nullable = True)
    home_planet = db.Column(db.String(150))
    super_power= db.Column(db.String(150))
    date_created = db.Column(db.Date)
    villian_or_hero = db.Column(db.String(8))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, super_hero_name, secret_identity, home_planet, villian_hero, user_token):
        self.super_hero_name = super_hero_name
        self.secret_identity = secret_identity
        self.home_planet = home_planet
        self.villian_or_hero = villian_hero
        self.user_token = user_token

    def __repr__(self):
            return f"The following Drone has been added: {self.super_hero_name}"

    def set_id(self):
        return secrets.token_urlsafe()

class SupeSchema(ma.Schema):
    class Meta: 
        fields = ['id', 'super_hero_name', 'secret_identity', 'home_planet', 'villian_or_hero']

Supe_schema = SupeSchema()
Supes_schema = SupeSchema(many = True)


    

    