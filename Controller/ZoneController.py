from Model.Zone import Zone
from Config import db


class ZoneController:

    @staticmethod
    def Add_Zone(data):
        NewZone = Zone(
            name=data["name"]
        )
        db.session.add(NewZone)
        db.session.commit()
        return f"New Zone is Added Successfully"

    @staticmethod
    def show_zone():
        Zones = Zone.query.all()

        return [{"Zone_name": zone.name} for zone in Zones]

