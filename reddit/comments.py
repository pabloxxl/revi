DEBUG = False
from request import request
from rObject import rObject


class comments(rObject):
    """
    Representation of reddit comments
    Args:
        uLink (string): link to comments pages
    """
    def __init__(self, uLink):
        if DEBUG:
            print "comments::__init__"
            print "\t"+uLink

    def dump(self):
        """Dump request object"""
        self.rOverview.dump()
