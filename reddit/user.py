from request import request
from rObject import rObject

import logging as lg


class user(rObject):
    """
    Representation of reddit user
    Args:
        uName (string): user name
    """
    def __init__(self, uName):
        lg.debug("user::__init__ " +
                 uName)

        self.uName = uName
        rTxtOverview = 'user/'+uName+'/overview/'
        self.rOverview = request(rTxtOverview)

    def dump(self):
        """Dump request object"""
        lg.debug("user::dump")
        self.rOverview.dump()

    def describe(self):
        """Print user description"""
        return "USER: " + self.uName
