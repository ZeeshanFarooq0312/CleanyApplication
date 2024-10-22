from Controller.TruckController import TruckController
from Controller.ZoneController import ZoneController
from Controller.UserController import UserController
from Controller.pickupcontroller import pickuprequestController
from Controller.UserZoneController import UserzoneController
from Controller.TruckAssigmentController import TruckAssigmentController
from Controller.SlotController import SlotController
from Controller.TruckscheduleController import TruckscheduleController
from Config import app, db
from flask import request, jsonify


@app.route("/addtruck", methods=["POST"])
def NewTruck():
    data = request.get_json()
    return jsonify(TruckController.Add_Truck(data))


@app.route("/adduser", methods=["POST"])
def NewUser():
    data = request.get_json()
    return jsonify(UserController.Add_User(data))

@app.route("/login_User",methods = ["POST"])
def Login_User():
    data = request.get_json()
    return jsonify(UserController.login(data))

@app.route("/newzone", methods=["POST"])
def NewZone():
    data = request.get_json()
    return jsonify(ZoneController.Add_Zone(data))


@app.route("/newpickup", methods=["POST"])
def NewPickup():
    data = request.get_json()
    return jsonify(pickuprequestController.Add_Pickup(data))


@app.route("/showdrivers")
def ShowDriver():
    return jsonify(UserController.Show_Driver())


@app.route("/showzones")
def ShowZone():
    return jsonify(ZoneController.show_zone())


@app.route("/showcollectors")
def ShowCollector():
    return jsonify(UserController.Show_Collector())


@app.route("/showoperators")
def ShowOperator():
    return jsonify(UserController.Show_Operator())

@app.route("/showuserzone")
def Show_UserZone():
    return jsonify(UserzoneController.Show_ALL_UserZone())


@app.route("/Truckschedule")
def Show_Truckschedules():
    return jsonify (TruckscheduleController.show_Truckschedule())




@app.route("/showSlot")
def Show_Slots():
    return jsonify(SlotController.ShowSlots())




@app.route("/AddTruckAssigment" , methods = ["POST"])
def NewTruckAssigment():
    data = request.get_json()
    return jsonify(TruckAssigmentController.Add_TruckAssigment(data))








@app.route("/showTruckAssigment")
def Show_TruckAssigment():
    return jsonify(TruckAssigmentController.show_truckAssigments())


@app.route("/deleteUser", methods=["POST"])
def Inactive_User():
    data = request.get_json()
    email = data["email"]
    if not email:
        return f"email is required"
    return jsonify(UserController.inactive_user(email))



@app.route("/changetruckStaff" , methods = ["POST"])
def Change_Truck_Staff():
    data = request.get_json()
    return jsonify(TruckAssigmentController.Change_TruckAssigment(data))

@app.route("/showtruckassigmentbydate",methods = ["POST"])
def Show_Assigment_BY_Date():
    data = request.get_json()
    return jsonify(TruckAssigmentController.Check_Assigment_By_Date(data))

@app.route("/InactiveTruckAssigments",methods = ["POST"])
def InactiveTruckAssigments():
    data = request.get_json()
    return jsonify(TruckAssigmentController.Inactive_TruckAssigments(data))

@app.route("/AutoTruckScheduling",methods = ["POST"])
def Auto_Truck_Schedules():
    data = request.get_json()
    return jsonify(TruckscheduleController.Auto_Schedule_Pickup_to(data))

@app.route("/UpdateTruckSequence",methods = ["POST"])
def update_Truck_Sequence():
    data = request.get_json()
    return jsonify(TruckscheduleController.Update_Sequence_Number(data))

@app.route("/Allinactiveusers")
def Inactive_user():
    return jsonify(UserController.Show_inactive_user())







@app.route("/Showtruckpickupdetail", methods = ["POST"])
def View_Truck_Pickup_detail():
    data = request.get_json()
    return jsonify(TruckscheduleController.show_truck_route(data))


@app.route("/ShowInactiveTrucks")
def show_Inactive_truck():
    return jsonify(TruckAssigmentController.Inactive_trucks())












if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
