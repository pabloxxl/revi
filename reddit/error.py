from rObject import rObject
import logging as lg


mapping_error = {
    0: "REVI INTERNAL ERROR",
    403: "FORBIDDEN",
    404: "PAGE NOT FOUND",
    500: "INTERNAL SERVER ERROR",
    503: "SERVICE UNAVAILABLE",
    504: "GATEWAY TIMEOut"
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

    def describe(self):
        """Print error  description"""
        return "ERROR: " + str(self.code)

    def dump(self):
        lg.debug("error::dump")

    def str(self):
        """ Return string describing error"""
        desc = mapping_error.get(self.code, "OTHER REASON")

        return ("Reddit returned code " + str(self.code) +
                " (" + desc + ")")
