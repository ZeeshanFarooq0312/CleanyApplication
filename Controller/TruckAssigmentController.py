from Config import db
from Model.TruckAssignment import TruckAssignment
from Model.User import User
from datetime import datetime
from Model.Truck import Truck
from sqlalchemy import func
class TruckAssigmentController:

    @staticmethod
    def  show_truckAssigments():
        TruckAssignments = TruckAssignment.query.all ()
        return [{"Truck id " : truck.truckid , "Zoneid ":truck.zoneid , "Collector id ":truck.collectorid , "Driver id ":truck.driverid }for truck in TruckAssignments]


    @staticmethod
    def Add_TruckAssigment(data):



        New_TruckAssigment = TruckAssignment (
            truckid = data["truckid"],
            zoneid = data["zoneid"],
            driverid = data["driverid"],
            collectorid = data["collectorid"]

        )
        db.session.add(New_TruckAssigment)
        db.session.commit()

        return {"Message":"Staff Assign to Truck successfully "} , 201

    @staticmethod
    def Change_TruckAssigment(data):
        Checked  = TruckAssignment.query.filter_by(truckid = data["truckid"] , status = 'active').first()

        if Checked :
            Checked.status = 'inactive'
            db.session.commit()

        Updated_Assigmnet = TruckAssignment(

                truckid = data["truckid"],
                zoneid=data["zoneid"],
                driverid=data["driverid"],
                collectorid=data["collectorid"],
                assignmentdate=func.current_date(),
                status='active'
            )
        db.session.add(Updated_Assigmnet)
        db.session.commit()
        return {"Message ":"Staff Updated to the Truck"},201

    @staticmethod
    def Check_Assigment_By_Date(data):

        try:
            date = datetime.strptime(data["assignmentdate"],"%Y-%m-%d").date()
        except ValueError:
             return {"Message Invalid date formate , date formate YY-MM-DD"} ,404



        Trucks = TruckAssignment.query.filter_by(assignmentdate = data["assignmentdate"]) .all()
        if Trucks:
            return [{"truck_id":truck.truckid , "zone_id":truck.zoneid , "driver_id" : truck.driverid , "collector_id":truck.collectorid, "Status" : truck.status}for truck in Trucks],200
        return {"Message" :"No  Truck Staff Assigment for this Date"} ,404

    @staticmethod
    def Inactive_TruckAssigments(data):
      Trucks = TruckAssignment.query.filter_by(status = data["status"]).all()
      if Trucks:
          return [{"truck_id": truck.truckid, "zone_id": truck.zoneid, "driver_id": truck.driverid,
                   "collector_id": truck.collectorid, "Status": truck.status ,"Assigment_Date" : truck.assignmentdate} for truck in Trucks], 200
      return {"Message": "Staff is not changed  on the Truck "}, 404

    @staticmethod
    def Inactive_trucks():
        inactive = TruckAssignment.query.filter_by(status='inactive').all()
        if inactive:
            return [{"truck_id": truck.truckid, "zone_id": truck.zoneid, "driver_id": truck.driverid,
                     "collector_id": truck.collectorid, "Status": truck.status, "Assigment_Date": truck.assignmentdate}
                    for truck in inactive], 200
        return {"Massage": "no Inactive trucks "},404






