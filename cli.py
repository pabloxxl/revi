import curses

from eval import cmd
from eval_vim import eval_vim
from reddit.listing import listing


class window:
    """
    Representation of main window of client
    Creating this object will init curses screen and set it to defaults
    """
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        curses.curs_set(0)

        self.maxY, self.maxX = self.stdscr.getmaxyx()

        self.currObject = listing("")

        self.eval = eval_vim(self.stdscr)

    def drawListing(self):
        """Draw list of links"""
        for i, link in enumerate(self.currObject.links):
            if i is self.currObject.currLine:
                for j in range(self.maxX-1):
                    self.stdscr.addstr(i, j, " ",
                                       curses.A_REVERSE)

                self.stdscr.addstr(i, 0, link.title.encode('utf-8'),
                                   curses.A_REVERSE)
            else:
                for j in range(self.maxX-1):
                    self.stdscr.addstr(i, j, " ")
                self.stdscr.addstr(i, 0, link.title.encode('utf-8'))

    def drawEval(self):
        """Draw object specific to eval objects (key mappings)"""
        self.eval.draw(self.maxY, self.maxX)

    def drawError(self):
        """Print error text"""
        self.stdscr.addstr(0, 0, "ERROR")
        self.stdscr.addstr(0, 1, "Unhandled: "+type(self.currObject).__name__)

    def draw(self):
        """(Re)draws entire screen"""
        # XXX Error handling???

        currObjectType = type(self.currObject).__name__
        if currObjectType == "listing":
            self.drawListing()
        else:
            self.drawError()

        self.drawEval()

    def processCmd(self):
        """
        Process cmd returned from eval_* object
        Returns:
            (bool): False if while loop has to exit. True otherwise
        """

        if self.cmd is cmd.QUIT:
            self.close()
            return False

        elif self.cmd is cmd.SWITCH_TO_COMMAND:
            curses.curs_set(1)

        elif self.cmd is cmd.SWITCH_TO_NORMAL:
            curses.curs_set(0)

        elif self.cmd is cmd.DOWN:
            self.currObject.increment()

        elif self.cmd is cmd.UP:
            self.currObject.decrement()
        return True

    def run(self):
        """
        Enter infinite loop, catch keys and process them.
        If eval object returns something other than None, process cmd object
        """
        while(True):
            self.draw()
            self.cmd = self.eval.eval()
            if self.cmd is not None:
                if not self.processCmd():
                    break

    def close(self):
        """
        Clean-up and close curses window.
        This method will be automaticaly called by class destructor
        """
        curses.nocbreak()
        curses.echo()
        self.stdscr.keypad(0)

        curses.endwin()
