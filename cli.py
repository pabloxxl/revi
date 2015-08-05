import curses

from eval import evalNormal
from eval import evalCommand
from eval import cmd


class mode:
    """This imitates vi modes, except visual and visual-block"""
    NORMAL, COMMAND, INSERT = range(3)


class window:
    """
    Representation of main window of client
    Creating this object will init curses screen and set it to defaults
    """

    def drawFooter(self):
        """Draw menu on the bottom of screen"""
        if self.mode is mode.COMMAND:
            self.stdscr.addstr(self.maxY-1, 0, ":"+self.text)
        elif self.mode is mode.NORMAL:
            # XXX I'm sure there is other method to do it...
            for i in range(self.maxX-1):
                self.stdscr.addstr(self.maxY-1, i, " ")

    def updateAndDraw(self):
        """(Re)draws entire screen"""
        # XXX Error handling???
        self.drawFooter()

    def getCmd(self):
        """
        Gets key from user input
        In normal mode, keys are parsed right after press
        Returns:
            (bool): False if program has to exit (e.g. ZZ or :q)
        """
        if self.mode is mode.NORMAL:
            self.prevChar = self.char
            self.char = self.stdscr.getch()

            self.cmd = evalNormal(chr(self.char), chr(self.prevChar))

        elif self.mode is mode.COMMAND:
            self.char = self.stdscr.getch()
            if self.char is ord("\n"):
                self.cmd = evalCommand(self.text)
                self.text = ""
            else:
                self.text += chr(self.char)
        return True

    def eval(self):
        """
        Evaluates command fetched from any mode
        Returns:
            (bool): False if program has to exit
        """

        if self.cmd is cmd.QUIT:
            self.close()
            return False
        elif self.cmd is cmd.SWITCH_TO_COMMAND:
            self.mode = mode.COMMAND
            self.char = 0
            self.prevChar = 0
            curses.curs_set(1)

        elif self.cmd is cmd.SWITCH_TO_NORMAL:
            self.cmd = ""
            curses.curs_set(0)
            self.mode = mode.NORMAL
        return True

    def __init__(self):
        self.mode = mode.NORMAL
        self.cmd = ""
        self.text = ""
        self.cmd = None

        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        curses.curs_set(0)

        self.prevchar = 0
        self.char = 0

        self.maxY, self.maxX = self.stdscr.getmaxyx()

    def close(self):
        """
        Clean-up and close curses window.
        This method will be automaticaly called by class destructor
        """
        curses.nocbreak()
        curses.echo()
        self.stdscr.keypad(0)

        curses.endwin()
