DEBUG = False
from request import request
from rObject import rObject


class user(rObject):
    """
    Representation of reddit user
    Args:
        uName (string): user name
    """
    def __init__(self, uName):
        if DEBUG:
            print "user::__init__"
            print "\t"+uName

        rTxtOverview = 'user/'+uName+'/overview/'
        self.rOverview = request(rTxtOverview)

    def dump(self):
        """Dump request object"""
        self.rOverview.dump()
