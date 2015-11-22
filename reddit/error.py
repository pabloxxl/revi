from rObject import rObject
import logging as lg


mapping_error = {
    0: "REVI INTERNAL ERROR",
    403: "FORBIDDEN",
    404: "PAGE NOT FOUND",
    500: "INTERNAL SERVER ERROR",
    503: "SERVICE UNAVAILABLE",
    504: "GATEWAY TIMEOUT"
}


class error(rObject):
    """
    Representation of reddit error
    Args:
        code (int): error code
    """
    def __init__(self, code=0):
        self.code = code
        lg.debug("%d", self.code)

    def decrement(self):
        lg.debug("")

    def increment(self):
        lg.debug("")

    def top(self):
        lg.debug("")

    def bottom(self):
        lg.debug("")

    def describe(self):
        """Print error  description"""
        return "ERROR: " + str(self.code)

    def dump(self):
        lg.debug("")

    def str(self):
        """ Return string describing error"""
        desc = mapping_error.get(self.code, "OTHER REASON")

        return ("Reddit returned code " + str(self.code) +
                " (" + desc + ")")
