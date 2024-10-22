from Model.PickupRequests import PickupRequests
from Model .UserZone import UserZone
from Model .User import User
from Model .Zone import Zone
from Config import db


class pickuprequestController:

    @staticmethod
    def Add_Pickup(data):

        # Check if all required fields are provided
        if "address" not in data or "phonenumber" not in data or "zone" not in data or "pickupdays" not in data or "email" not in data:
            return {"Message": "Incomplete Information Provided for Pickup request"}, 404

        # Find the user by email
        user = User.query.filter_by(email=data["email"]).first()
        if not user:
            return {"Message": "No User Found with this email"}, 404

        # Find the zone by name
        zone = Zone.query.filter_by(name=data["zone"]).first()
        if not zone:
            return {"Message": "No Such Zone Found"}, 404

        # Check if the user is already associated with the zone
        existing_user_zone = UserZone.query.filter_by(userid=user.id, zoneid=zone.id).first()
        if not existing_user_zone:
            # Add the user to the zone if not already added
            new_user_zone = UserZone(
                userid=user.id,
                zoneid=zone.id
            )
            db.session.add(new_user_zone)
            db.session.commit()

        # Step 1: Check if "pickupdays" is a string or list
        pickup_days = data["pickupdays"]

        # If the user provides only one day, convert it to a list for uniform handling
        if isinstance(pickup_days, str):
            pickup_days = [pickup_days]  # Convert single string to a list

        # Step 2: Loop through each pickup day in the list and create a new pickup request for each day
        for day in pickup_days:
            newpickup = PickupRequests(
                userid=user.id,
                address=data["address"],
                phonenumber=data["phonenumber"],
                pickupday=day  # Assign each day from the list (or the single day)
            )
            db.session.add(newpickup)

        # Commit the changes after all entries are added
        db.session.commit()

        return {"Message": "Pickup requests placed successfully for multiple days" if len(
            pickup_days) > 1 else "Pickup request placed successfully"}, 201




