from Config import db
from sqlalchemy import Enum

class User(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, index=True)  # Index on email
    password = db.Column(db.String(100), nullable=False)
    phonenumber = db.Column(db.String(11), nullable=False)
    address = db.Column(db.String(255), nullable=True)  # Address is nullable
    role = db.Column(Enum('user', 'driver', 'operator', 'collector', name='user_roles'), nullable=False)
    status = db.Column(Enum('active', 'inactive', name='user_status'), nullable=False, server_default='active')
    zoneid = db.Column(db.Integer, db.ForeignKey("Zone.id"), nullable=True, index=True)

    zone = db.relationship('Zone', backref='User')


