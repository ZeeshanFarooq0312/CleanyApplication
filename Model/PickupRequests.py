from Config import db
from sqlalchemy import Enum


class PickupRequests(db.Model):
    __tablename__ = "pickuprequest"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(255), nullable=False)
    phonenumber = db.Column(db.String(11), nullable=False)
    pickupday = db.Column(db.String(50), nullable=False)
    status = db.Column(Enum("pending", "completed", name="pickupstatus"), nullable=False,
                       server_default="pending")
    userid = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False, index=True)

    user = db.relationship("User", backref="pickuprequest")


