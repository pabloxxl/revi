import logging as lg


class sortType:
    """ Enumeration of listing sorting types. Used in listing constructor"""
    HOT, NEW, RISING, CONTROVERSIAL, TOP, GILDED, WIKI, PROMOTED = range(8)


def typeStr(type):
    """
    Converts number (represented as class sortType variable) to string
    Args:
        type (sortType): sortType member
    Returns:
        string : Text representation of type number
    """
    if type is sortType.HOT:
        return "hot"
    elif type is sortType.RISING:
        return "rising"
    elif type is sortType.CONTROVERSIAL:
        return "controversial"
    elif type is sortType.TOP:
        return "top"
    elif type is sortType.GILDED:
        return "gilded"
    elif type is sortType.WIKI:
        return "wiki"
    elif type is sortType.PROMOTED:
        return "promoted"
    else:
        return ""


class rObject(object):
    """
    Common ancestor for all reddit objects
    """
    def decrease(self):
        lg.debug("rObject::decrease")

    def increase(self):
        lg.debug("rObject::increase")

    def top(self):
        lg.debug("rObject::top")

    def bottom(self):
        lg.debug("rObject::bottom")
