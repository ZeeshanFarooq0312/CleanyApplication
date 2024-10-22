from Config import db
from Model.User import User
from Model.Zone import Zone




class UserController:

    @staticmethod
    def Add_User(data):
        role = data.get("role", "User")

        if role not in ["User", "Driver", "Operator", "Collector"]:
            raise ValueError("Invalid role entered")
        if data["password"]!= data["confirmpassword"]:
            raise ValueError("Password and conformpassword Miss match")

        zoneid = None

        if role == "User":
            if not data.get("address") or not data.get("zonename"):
                raise ValueError("Address and zone name are mandatory")

            zone = Zone.query.filter_by(name=data["zonename"]).first()
            if not zone:
                raise ValueError("Incorrect Zone Name")

            zoneid = zone.id

        else:
            zoneid = data.get("zoneid")

        new_user = User(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            phonenumber=data["phonenumber"],
            address=data.get("address"),
            role=role,
            status=data.get("status", "active"),
            zoneid=zoneid
        )

        db.session.add(new_user)
        db.session.commit()

        return f"New {role} is added successfully"



    @staticmethod
    def login(data):
       user = User.query.filter_by(email = data["email"]).first()
       if user:
            if data["password"]==user.password:
                if user.status == 'active':
                    return {"message":"Login Successfully"},201
                else:
                    return {"message":"your account is inactive contact support Center "},404
            else:
                return {"message":"incorrect password entered"},404
       else:
          return {"message" : "No Account with this email"},404




    @staticmethod
    def Show_Driver():
        Driver = User.query.filter_by(role="Driver").all()
        return [
            {"Driver id": driver.id, "Driver Name": driver.name, "Driver Email": driver.email}
            for driver in Driver]

    @staticmethod
    def Show_Collector():
        Collector = User.query.filter_by(role="Collector").all()
        return [{"Collector Email ": collector.email, "Collector Name": collector.name, "Collector Id ": collector.id}
                for collector in Collector]

    @staticmethod
    def Show_Operator():
        Operators = User.query.filter_by(role="Operator").all()
        return [{"Operator Email ": operator.email, "Operator Name": operator.name, "Operator Id ": operator.id}
                for operator in Operators]
    @staticmethod
    def Show_inactive_user():
        Users  = User.query.filter_by(status = 'inactive').all()
        return [{"User Email ": user.email, "User Name": user.name, "User Id ": user.id}
                for user in Users]

    @staticmethod
    def inactive_user(email):

        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError("no record found")
        if user.status == "inactive":
            raise ValueError("user is Inactive already")

        user.status = "inactive"
        db.session.commit()
        return f"{user.name} your account is Inactivated"
