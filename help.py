import logging as lg


class help(object):
    """
    Wrapper class around various help lists
    """
    vim_command = [
        ("q | quit", "Quit program"),
        ("h | help", "Display help screen"),
        ("license ", "Display license screen"),
        ("history ", "Display overview of last undo / redo operations")
    ]

    vim_normal = [
        (": ", "Enter command mode"),
        ("i ", "Enter insert mode"),
        ("j ", "Go one line down"),
        ("k ", "Go one line up"),
        ("b ", "Go one page backward"),
        ("w ", "Go one page forward"),
        ("B ", "Go to first visited page"),
        ("W ", "Return from first visited page"),
        ("G ", "Go to bottom"),
        ("gg", "Go to top"),
        ("ZZ", "Quit program"),
        ("\\n", "Follow current link")
    ]

    emacs = [
        ("STUB", "STUB")
    ]

    def __init__(self):
        lg.debug("Initialized help")

    def increment(self):
        pass

    def decrement(self):
        pass

    def top(self):
        pass

    def bottom(self):
        pass

    def describe(self):
        return "HELP"
