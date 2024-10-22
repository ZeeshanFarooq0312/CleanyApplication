from Config import db
from sqlalchemy import Enum


class Slot(db.Model):
    __tablename__ = "Slot"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dayofweek = db.Column(Enum("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"), nullable=False)
    starttime = db.Column(db.Time, nullable=False)
    endtime = db.Column(db.Time, nullable=False)
