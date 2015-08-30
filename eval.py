import logging as lg


class cmd:
    """ Commands, returned to cli.py as response for text"""
    QUIT = 0
    SWITCH_TO_NORMAL = 1
    SWITCH_TO_COMMAND = 2  # params: p
    SWITCH_TO_INSERT = 3
    ENTER = 4  # params: p1, p2
    ENTER_EXTERNAL = 5
    DOWN = 20
    UP = 21
    TOP = 22
    BOTTOM = 23
    BACK = 24
    FORWARD = 25
    BACK_ABSOLUTE = 26
    FORWARD_ABSOLUTE = 27
    HELP = 30
    HISTORY = 31
    LICENSE = 32
    NONE = 99

    def __init__(self, id=NONE, *args):
        """
        Holder for command returned from eval
        Arguments:
            id(int)[cmd.NONE]: command numeric value
        """
        lg.debug("cmd::__init " + str(id))
        self.id = id
        self.args = args
        if args is not None:
            for i, arg in enumerate(args):
                lg.debug("p[" + str(i) + "]: " + arg)


class eval(object):
    """ Parent class for all eval object (diferent key mappings """
    def draw(self, maxY, maxX):
        """
        Container method to all draw methods defined in eval class
        Arguments:
            maxY(int): window height
            maxX(int): windows width
        """
        lg.debug("eval::draw")
