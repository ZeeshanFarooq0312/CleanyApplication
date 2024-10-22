from Config import db
class Truckschedule(db.Model):
    __tablename__ = "truckschedule"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    truckid = db.Column(db.Integer, db.ForeignKey("Truck.id"), nullable=False, index=True)
    scheduleid = db.Column(db.Integer, db.ForeignKey("Slot.id"), nullable=False, index=True)
    sequencenumber = db.Column(db.Integer, nullable=False)
    pickuprequestid = db.Column(db.Integer, db.ForeignKey("pickuprequest.id"), nullable=False, index=True)


    truck = db.relationship("Truck", backref="truckschedules")
    schedule = db.relationship("Slot", backref="truckschedules")
    pickuprequest = db.relationship("PickupRequests", backref="truckschedules")  # Correct class name
