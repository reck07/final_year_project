from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Crop(db.Model):
    __tablename__ = 'crops'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    optimal_n = db.Column(db.Float)
    optimal_p = db.Column(db.Float)
    optimal_k = db.Column(db.Float)
    optimal_temperature = db.Column(db.Float)
    optimal_humidity = db.Column(db.Float)
    optimal_ph = db.Column(db.Float)
    optimal_rainfall = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    input_data = db.Column(db.JSON)
    output_data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    user = db.relationship('User', backref=db.backref('recommendations', lazy=True)) 