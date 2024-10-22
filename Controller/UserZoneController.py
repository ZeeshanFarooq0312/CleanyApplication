from Model.UserZone import UserZone
from Config import db
class UserzoneController:

    @staticmethod
    def Show_ALL_UserZone():
        userzones = UserZone.query.all()
        return [ {"username ": userzone.userid , "userZone " : userzone.zoneid}for userzone in userzones]
