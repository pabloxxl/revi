class cmd:
    """ Commands, returned to cli.py as response for text"""
    QUIT = 0
    SWITCH_TO_NORMAL = 1
    SWITCH_TO_COMMAND = 2
    SWITCH_TO_INSERT = 3
    DOWN = 21
    UP = 22


class eval(object):
    """ Parent class for all eval object (diferent key mappings """
    def draw(self, maxY, maxX):
        """
        Container method to all draw methods defined in eval class
        Arguments:
            maxY(int): window height
            maxX(int): windows width
        """
        pass
