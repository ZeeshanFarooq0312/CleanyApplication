from Config import db
from sqlalchemy import func
from sqlalchemy import Enum
class TruckAssignment(db.Model):
    __tablename__ = "Truckassignment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    truckid = db.Column(db.Integer, db.ForeignKey("Truck.id"), nullable=False, index=True)
    zoneid = db.Column(db.Integer, db.ForeignKey("Zone.id"), nullable=False, index=True)
    collectorid = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False, index=True)  # ForeignKey to User table
    driverid = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False, index=True)    # ForeignKey to User table
    assignmentdate = db.Column(db.Date, nullable=False, server_default=func.current_date())
    status = db.Column(Enum('active' , 'inactive') , nullable= False ,server_default = 'active')

    collector = db.relationship("User", foreign_keys=[collectorid], backref="collector_assignments")
    driver = db.relationship("User", foreign_keys=[driverid], backref="driver_assignments")
    truck = db.relationship("Truck", backref="truck_assignments")
    zone = db.relationship("Zone", backref="truck_assignments")


