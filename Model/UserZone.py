from Config import db


class UserZone(db.Model):
    __tablename__ = "userzone"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    zoneid = db.Column(db.Integer, db.ForeignKey("Zone.id"), nullable=False)

    user = db.relationship("User", backref="userzone")
    zone = db.relationship("Zone", backref="userzone")
