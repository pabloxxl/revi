class cmd:
    """ Commands, returned to cli.py as response for text"""
    QUIT = 0
    SWITCH_TO_NORMAL = 1
    SWITCH_TO_COMMAND = 2
    SWITCH_TO_INSERT = 3
    DOWN = 21
    UP = 22


def evalCommand(text):
    """
    Evaluate command (string) stated in normal mode
    Arguments:
        text(string): text stated after ":" sign
    Returns:
        (cmd): command object
    """
    if text == "q":
        return cmd.QUIT
    elif text == "quit":
        return cmd.QUIT
    else:
        return cmd.SWITCH_TO_NORMAL


def evalNormal(char, prevChar):
    """
    Evaluate char (and preceding char) used in normal mode
    Arguments:
        char(string): pressed key
        prevChar(string): previously pressed key
    Returns:
        (cmd): command object
    """
    if char is ':':
        return cmd.SWITCH_TO_COMMAND
    elif char is 'i':
        return cmd.SWITCH_TO_INSERT
    elif char is 'j':
        return cmd.DOWN
    elif char is 'k':
        return cmd.UP
    elif char is 'Z' and prevChar is 'Z':
        return cmd.QUIT
