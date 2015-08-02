import curses


class mode:
    """This imitates vi modes, except visual and visual-block"""
    NORMAL, COMMAND, INSERT = range(3)


class window:
    """
    Representation of main window of client
    Creating this object will init curses screen and set it to defaults
    """

    def drawMenu(self):
        """Draw menu on the bottom of screen"""
        if self.mode is mode.COMMAND:
            self.stdscr.addstr(self.maxY-1, 0, ":"+self.cmd)
        elif self.mode is mode.NORMAL:
            # XXX I'm sure there is other method to do it...
            for i in range(self.maxX-1):
                self.stdscr.addstr(self.maxY-1, i, " "+self.cmd)

    def updateAndDraw(self):
        """(Re)draws entire screen"""
        # XXX Error handling???
        self.drawMenu()

    def getChar(self):
        """
        Gets key from user input
        In normal mode, keys are parsed right after press
        Returns:
            (bool): False if program has to exit (e.g. ZZ or :q)
        """
        if self.mode is mode.NORMAL:
            self.prevchar = self.char
            self.char = self.stdscr.getch()

            if self.char is ord(':'):
                self.mode = mode.COMMAND
                curses.curs_set(1)
            elif self.char is ord('j'):
                # DOWN
                pass
            elif self.char is ord('k'):
                # UP
                pass
            elif self.char is ord('Z') and self.prevchar is ord('Z'):
                self.close()
                return False
        elif self.mode is mode.COMMAND:
            self.char = self.stdscr.getch()
            if self.char is ord("\n"):
                return self.evalCmd()
            else:
                self.cmd += chr(self.char)
        return True

    def evalCmd(self):
        """
        Evaluates command fetched from COMMAND mode
        Returns:
            (bool): False if program has to exit (:q)
        """
        if self.cmd is 'q':
            self.close()
            self.cmd = ""
            return False
        self.cmd = ""
        curses.curs_set(0)
        self.mode = mode.NORMAL
        return True

    def __init__(self):
        self.mode = mode.NORMAL
        self.cmd = ""

        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        curses.curs_set(0)

        self.prevchar = 0
        self.char = 0

        self.maxY, self.maxX = self.stdscr.getmaxyx()

#    def __del__(self):
#        self.close()

    def close(self):
        """
        Clean-up and close curses window.
        This method will be automaticaly called by class destructor
        """
        curses.nocbreak()
        curses.echo()
        self.stdscr.keypad(0)

        curses.endwin()
