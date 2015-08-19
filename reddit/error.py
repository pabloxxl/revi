from rObject import rObject
import logging as lg


mapping_error = {
    404: "Reddit returned code 404 (page not found)"
}


class error(rObject):
    """
    Representation of reddit error
    Args:
        code (int): error code
    """
    def __init__(self, code=0):
        self.code = code
        lg.debug("error::__init__ " +
                 str(self.code))

    def decrement(self):
        lg.debug("error::decrement")

    def increment(self):
        lg.debug("error::increment")

    def top(self):
        lg.debug("error::top")

    def bottom(self):
        lg.debug("error::bottom")

    def dump(self):
        lg.debug("error::dump")

    def describe(self):
        """ Return string describing error"""
        return mapping_error.get(self.code, "Undefined error")