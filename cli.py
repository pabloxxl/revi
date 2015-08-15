import curses

from eval import cmd
from eval_vim import eval_vim
from reddit.listing import listing
from reddit.comments import comments

import logging as lg


class window:
    """
    Representation of main window of client
    Creating this object will init curses screen and set it to defaults
    """
    def __init__(self):
        lg.debug("cli::__init__")
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        curses.curs_set(0)

        self.maxY, self.maxX = self.stdscr.getmaxyx()

        self.MAX_LIST_ITEMS = self.maxY - 3

        lg.debug("Maximum number for items is " +
                 str(self.MAX_LIST_ITEMS))

        self.drawLoading()

        self.currObject = listing("", rLimit=self.MAX_LIST_ITEMS)
        self.clear()
        self.eval = eval_vim(self.stdscr)

    def drawListing(self):
        """Draw list of links"""
        lg.debug("cli::drawListing")
        # Should change to subredit title
        self.stdscr.addstr(0, 0, "FRONTPAGE:")
        for i, link in enumerate(self.currObject.links, start=1):
            if i > self.MAX_LIST_ITEMS:
                lg.warning("Reached end of screen with links " +
                           "left to draw (" +
                           str(len(self.currObject.links)-i) + ")")
                break
            if i is self.currObject.currLine+1:
                for j in range(self.maxX-1):
                    self.stdscr.addstr(i, j, " ",
                                       curses.A_REVERSE)

                self.stdscr.addstr(i, 0, link.title.encode('utf-8'),
                                   curses.A_REVERSE)
            else:
                for j in range(self.maxX-1):
                    self.stdscr.addstr(i, j, " ")
                self.stdscr.addstr(i, 0, link.title.encode('utf-8'))

    def drawComments(self):
        """Draw list of comments"""
        lg.debug("cli::drawComments")

        self.stdscr.addstr(0, 0, "COMMENTS:")
        for i, comment in enumerate(self.currObject.comments, start=1):
            if i > self.MAX_LIST_ITEMS:
                lg.warning("Reached end of screen with comments " +
                           "left to draw (" +
                           str(len(self.currObject.comments)-i) + ")")
                break
            if i is self.currObject.currComment+1:
                self.stdscr.addstr(i, 0, "[+]"+comment.author.encode('utf-8') +
                                   ": " + comment.text.encode('utf-8'))
            else:
                self.stdscr.addstr(i, 0, comment.author.encode('utf-8') +
                                   ": " + comment.text.encode('utf-8'))

    def drawEval(self):
        """Draw object specific to eval objects (key mappings)"""
        lg.debug("cli::drawEval")
        self.eval.draw(self.maxY, self.maxX)

    def drawError(self):
        """Print error text"""
        lg.debug("cli::drawError")
        self.clear()
        self.stdscr.addstr(0, 0, "ERROR")
        self.stdscr.addstr(1, 2, "Unhandled rObject type: " +
                           type(self.currObject).__name__)

    def drawLoading(self):
        """Print loading screen"""
        lg.debug("cli::drawLoading")
        self.clear()
        self.stdscr.addstr(self.maxY/2, self.maxX/2, "PLEASE STAND BY")
        self.stdscr.refresh()

    def draw(self):
        """(Re)draws entire screen"""
        lg.debug("cli::draw")
        # XXX Error handling???

        currObjectType = type(self.currObject).__name__
        if currObjectType == "listing":
            self.drawListing()
        elif currObjectType == "comments":
            self.drawComments()
        else:
            lg.warning("Tried to draw non-existing object Type: ",
                       currObjectType)
            self.drawError()

        self.drawEval()
        self.stdscr.refresh()

    def clear(self):
        """Clear entire screen"""
        lg.debug("cli::clear")
        self.stdscr.clear()

    def processCmd(self):
        """
        Process cmd returned from eval_* object
        Returns:
            (bool): False if while loop has to exit. True otherwise
        """
        lg.debug("cli::processCmd " +
                 str(self.cmd))

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

        elif self.cmd is cmd.TOP:
            self.currObject.top()

        elif self.cmd is cmd.BOTTOM:
            self.currObject.bottom()

        elif self.cmd is cmd.ENTER:
            currObjectType = type(self.currObject).__name__
            if currObjectType == "listing":
                self.drawLoading()
                self.followCurrent()
        return True

    def followCurrent(self):
        """Fetches link  from current cmd and tries to follow it."""
        lg.debug("cli::followCurrent " +
                 str(self.currObject.currLine))
        link = self.currObject.getLink(self.currObject.currLine)
        self.currObject = comments(link.addr, rLimit=self.MAX_LIST_ITEMS)
        self.clear()

    def run(self):
        """
        Enter infinite loop, catch keys and process them.
        If eval object returns something other than None, process cmd object
        """
        lg.debug("cli::run")
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
        lg.debug("cli::close")
        curses.nocbreak()
        curses.echo()
        self.stdscr.keypad(0)

        curses.endwin()
