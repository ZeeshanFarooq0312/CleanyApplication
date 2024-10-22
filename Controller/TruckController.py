from Model.Truck import Truck
from Config import db


class TruckController:

    @staticmethod
    def Add_Truck(data):
        newTruck = Truck(
            licensenumber=data["licensenumber"],
            model=data["model"],
            chassisnumber=data["chassisnumber"]
        )
        db.session.add(newTruck)
        db.session.commit()
        return f"truck Added Successfully"
