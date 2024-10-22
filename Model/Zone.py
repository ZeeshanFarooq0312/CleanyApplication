from Config import db


class Zone(db.Model):
    __tablename__ = "Zone"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

   