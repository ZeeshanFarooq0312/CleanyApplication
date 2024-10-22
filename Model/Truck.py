from Config import db


class Truck(db.Model):
    __tablename__ = "Truck"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    licensenumber = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    chassisnumber = db.Column(db.String(50), nullable=False)
