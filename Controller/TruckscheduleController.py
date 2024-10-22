from Model.Truckschedule import Truckschedule
from Model.UserZone import UserZone
from Model.Truck import Truck
from Model.PickupRequests import PickupRequests
from Model.TruckAssignment import TruckAssignment
from Model.Slot import Slot
from Config import db


class TruckscheduleController:

    @staticmethod
    def show_Truckschedule():
        Truckschedules = Truckschedule.query.all()
        return [{"Truck Id": Truckschedule.truckid,
                 "Schedule Id": Truckschedule.scheduleid,
                 "SequenceNumber": Truckschedule.sequencenumber,
                 "PickupRequest Id": Truckschedule.pickuprequestid}
                for Truckschedule in Truckschedules]

    @staticmethod
    def Auto_Schedule_Pickup_to(data):
        pickup_request_id = data["pickuprequestid"]
        sequence_number = data.get("sequencenumber")

        # Step 1: Get the pickup request by ID
        pickup_request = PickupRequests.query.filter_by(id=pickup_request_id).first()
        if not pickup_request:
            return {"Message": "No such Pickup_Request_Id found"}, 404

        # Step 2: Find the user's zone and truck assignment
        user_zone = UserZone.query.filter_by(userid=pickup_request.userid).first()
        if not user_zone:
            return {"Message": "No zone Selected by user for pickup"}, 404

        truck_assign = TruckAssignment.query.filter_by(zoneid=user_zone.zoneid).first()
        if not truck_assign:
            return {"Message": "No truck is assigned to your selected zone"}, 404

        # Step 3: Get available slots for the selected pickup day
        available_slots = Slot.query.filter_by(dayofweek=pickup_request.pickupday).all()
        if not available_slots:
            return {"Message": f"No slots available for {pickup_request.pickupday}"}, 404

        # Step 4: Check if the requested sequence number is valid
        if sequence_number < 1 or sequence_number > len(available_slots):
            return {
                "Message": f"Invalid sequence number. Please provide a number between 1 and {len(available_slots)}."}, 400

        # Step 5: Assign the slot based on the sequence number
        assigned_slot_id = available_slots[sequence_number - 1].id  # Get the slot corresponding to the sequence number

        # Step 6: Create a new schedule entry
        new_schedule = Truckschedule(
            truckid=truck_assign.truckid,
            pickuprequestid=pickup_request.id,
            scheduleid=assigned_slot_id,  # Assign the slot based on the sequence number
            sequencenumber=sequence_number
        )

        db.session.add(new_schedule)
        db.session.commit()

        return {"Message": "Truck, time slot, and sequence number successfully assigned to pickup request"}

    @staticmethod
    def Update_Sequence_Number(data):
        # Step 1: Get the pickup request by ID
        pickup_request_schedule = Truckschedule.query.filter_by(pickuprequestid=data["pickuprequestid"]).first()

        if not pickup_request_schedule:
            return {"Message": "No such Pickup Request ID found"}, 404

        # Step 2: Retrieve the pickup day from the PickupRequests table
        pickup_request = PickupRequests.query.filter_by(id=data["pickuprequestid"]).first()
        if not pickup_request:
            return {"Message": "Pickup request not found"}, 404

        pickup_day = pickup_request.pickupday  # Assuming pickup_day is the field representing the pickup day
        print(f"Pickup Day: {pickup_day}")

        # Step 3: Check for available slots for the retrieved day based on `dayofweek`
        available_slots = Slot.query.filter_by(dayofweek=pickup_day).order_by(Slot.id).all()

        if not available_slots:
            return {"Message": "No available slots for the requested day"}, 404

        new_sequence_number = data["sequencenumber"]

        try:
            # Step 4: Fetch all pickup requests for this truck on the same day, using the `dayofweek` from the Slot table
            requests_to_shift = db.session.query(Truckschedule).join(Slot, Truckschedule.scheduleid == Slot.id).filter(
                Truckschedule.truckid == pickup_request_schedule.truckid,
                Slot.dayofweek == pickup_day,  # Filter by the day of the week from the Slot table
                Truckschedule.sequencenumber >= new_sequence_number
            ).order_by(Truckschedule.sequencenumber).all()

            # Step 5: Shift sequence numbers and assign new slots for all requests
            for request in requests_to_shift:
                if request.pickuprequestid != data["pickuprequestid"]:  # Skip the one being updated
                    # Increment the sequence number
                    request.sequencenumber += 1

                    # Update the slot ID based on the new sequence number if within limits
                    if request.sequencenumber <= len(available_slots):
                        request.scheduleid = available_slots[request.sequencenumber - 1].id
                    else:
                        request.scheduleid = None  # Handle if there are no slots left

                    db.session.add(request)

            # Step 6: Assign the new pickup request the new sequence number and the first available slot
            pickup_request_schedule.sequencenumber = new_sequence_number
            pickup_request_schedule.scheduleid = available_slots[new_sequence_number - 1].id  # Assign the slot

            # Step 7: Commit the changes to the database
            db.session.commit()

            return {"Message": "Sequence number updated successfully"}, 200

        except Exception as e:
            db.session.rollback()
            return {"Message": f"Error updating sequence number: {str(e)}"}, 500
