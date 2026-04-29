from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), nullable=False, default="user")
    
    def __init__(self, username: str, password: str, role : str):
        self.username = username
        self.password = password
        self.role = role
        return f'<User {self.username}>'