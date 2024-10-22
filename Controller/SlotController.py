from Config import db
from Model.Slot import Slot


class SlotController:

    @staticmethod
    def ShowSlots():
        slots = Slot.query.all()
        return [
            {
                "Day": slot.dayofweek,
                "Start_Time": slot.starttime.strftime("%H:%M:%S"),
                "End_Time": slot.endtime.strftime("%H:%M:%S")
            }
            for slot in slots
        ]
