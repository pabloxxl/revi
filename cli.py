import curses

from eval import cmd
from eval_vim import eval_vim
from reddit.listing import listing
from reddit.comments import comments
from reddit.error import error
from help import help
from globals import mode
from history import history
import logging as lg
import os

BORDER_SIGN = "="
BORDER_SIGN_V = "|"

BOTTOM_OFFSET = 3


class window:
    """
    Representation of main window of client
    Creating this object will init curses screen and set it to defaults
    Arguments:
        config(dictionary): set of options read from config file
    """
    def __init__(self, config):
        lg.debug("cli::__init__")
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        curses.curs_set(0)

        self.maxY, self.maxX = self.stdscr.getmaxyx()

        self.MAX_LIST_ITEMS = self.maxY - BOTTOM_OFFSET - 2

        lg.debug("Maximum number for items is " +
                 str(self.MAX_LIST_ITEMS))
        self.MODE = mode.VIM

        hm = config.get("history_max", 5)

        self.browser = config.get("browser", None)
        self.history = history(hm)

        self.currObject = None

        self.msg = None
        self.setMsg("Revi started, config loaded from file, "
                    "word peace achieved")

        self.drawLoading()

        l = listing("", rLimit=self.MAX_LIST_ITEMS)
        if l.ok:
            self.setCurrentObject(l)
        else:
            self.setCurrentObject(error(l.status))

        if self.MODE is mode.VIM:
            self.eval = eval_vim(self.stdscr)
        else:
            # self.eval = eval_emacs(self.stdscr)
            pass

        self.help = help()

    def drawBorder(self):
        """Draw border"""
        lg.debug("cli::drawBorder")
        # TODO fetch version and name from variable
        title = "[[REVI v0.1]]"
        upper_border = BORDER_SIGN*(self.maxX - len(title) - 5) \
            + title + 5*BORDER_SIGN

        bottom_border = BORDER_SIGN*(self.maxX)

        self.stdscr.addstr(0, 0, upper_border)
        self.stdscr.addstr(self.maxY - BOTTOM_OFFSET, 0, bottom_border)

        for i in range(1, self.maxY - BOTTOM_OFFSET):
            self.stdscr.addstr(i, 0, BORDER_SIGN_V)
            self.stdscr.addstr(i, self.maxX - 1, BORDER_SIGN_V)

    def drawStatus(self):
        """Draw statusline"""
        lg.debug("cli::drawStatus")
        if self.msg is not None:
            self.stdscr.addstr(self.maxY - 2, 0, self.msg, curses.A_STANDOUT)
        else:
            self.stdscr.addstr(self.maxY - 2, 0, " "*(self.maxX - 1))

    def drawListing(self):
        """Draw list of links"""
        lg.debug("cli::drawListing")
        # Should change to subredit title
        self.stdscr.addstr(1, 1, "FRONTPAGE:")
        for i, link in enumerate(self.currObject.links, start=2):
            # This surely does nothing...
            # or does it? Have to check
            if i > self.MAX_LIST_ITEMS + 2:
                lg.warning("Reached end of screen with links " +
                           "left to draw (" +
                           str(len(self.currObject.links)-i) + ")")
                break
            if i is self.currObject.currLine+2:
                for j in range(1, self.maxX-1):
                    self.stdscr.addstr(i, j, " ",
                                       curses.A_REVERSE)

                self.stdscr.addstr(i, 1, link.title.encode('utf-8'),
                                   curses.A_REVERSE)
            else:
                for j in range(1, self.maxX-1):
                    self.stdscr.addstr(i, j, " ")
                self.stdscr.addstr(i, 1, link.title.encode('utf-8'))

    def drawComments(self):
        """Draw list of comments"""
        lg.debug("cli::drawComments")
        self.clear()  # I should consider not clearing here

        self.stdscr.addstr(1, 1, "COMMENTS(" +
                           str(self.currObject.getCurrentCommentNumber()) +
                           "/" + str(self.currObject.getNumberOfComments()) +
                           "):")
        comment = self.currObject.getCurrentComment()
        self.stdscr.addstr(3, 1, comment.author.encode('utf-8') +
                           ": ", curses.A_BOLD)

        self.stdscr.addstr(4, 1, comment.text.encode('utf-8'))

    def drawEval(self):
        """Draw object specific to eval objects (key mappings)"""
        lg.debug("cli::drawEval")
        self.eval.draw(self.maxY, self.maxX)

    def drawError(self):
        """Print error text"""
        lg.debug("cli::drawError")
        self.clear()
        self.stdscr.addstr(0, 0, "ERROR")
        self.stdscr.addstr(1, 0, self.currObject.str())

    def drawLoading(self):
        """Print loading screen"""
        lg.debug("cli::drawLoading")
        self.clear()
        self.drawBorder()
        self.stdscr.addstr(self.maxY/2, self.maxX/2, "PLEASE STAND BY")
        self.stdscr.refresh()

    def drawHelp(self):
        """Print help screen dependant on mode"""
        lg.debug("cli::drawLoading with mode: "+str(self.MODE))

        if self.MODE is mode.VIM:
            self.stdscr.addstr(0, 1, "HELP:")
            self.stdscr.addstr(2, 1, "VIM command mode bindings:",
                               curses.A_BOLD)
            line = 3
            for key, val in self.help.vim_command:
                self.stdscr.addstr(line, 1, key + " : " + val)
                line += 1

            line += 1
            self.stdscr.addstr(line, 1, "VIM normal mode bindings:",
                               curses.A_BOLD)
            line += 1
            for item in self.help.vim_normal:
                self.stdscr.addstr(line, 1, item[0] + " : " + item[1])
                line += 1

    def draw(self):
        """(Re)draws entire screen"""
        lg.debug("cli::draw")
        # XXX Error handling???

        currObjectType = type(self.currObject).__name__
        if currObjectType == "listing":
            self.drawListing()
        elif currObjectType == "comments":
            self.drawComments()
        elif currObjectType == "help":
            self.drawHelp()
        elif currObjectType == "error":
            self.drawError()

        self.drawBorder()
        self.drawEval()
        self.drawStatus()
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
                 str(self.cmd.id))

        self.clearMsg()

        # This should be more global. Dunno how to do that.
        mapping_cli = {
            cmd.QUIT: self.close,
            cmd.HELP: self.performHelp,
            cmd.DOWN: self.currObject.increment,
            cmd.UP: self.currObject.decrement,
            cmd.TOP: self.currObject.top,
            cmd.BOTTOM: self.currObject.bottom,
            cmd.BACK: self.performBack,
            cmd.ENTER: self.performEnter,
            cmd.ENTER_EXTERNAL: self.performExternalEnter
        }

        fun = mapping_cli.get(self.cmd.id, None)
        if fun is not None:
            fun()

        if self.cmd.id is cmd.QUIT:
            return False
        return True

    def performEnter(self):
        """Interpret ENTER key"""
        currObjectType = type(self.currObject).__name__
        if currObjectType == "listing":
            self.drawLoading()
            self.followCurrent()
            self.setMsg(str(self.currObject.getNumberOfComments()) +
                        " comments loaded")

    def performExternalEnter(self):
        if self.browser is None:
            lg.warning("Tried to open external link without browser set!")
        else:
            link = self.currObject.getLink(self.currObject.currLine)
            os.system("%s %s" % (self.browser, link.url))
            self.setMsg("Link loaded externaly")

    def performBack(self):
        """Interpret BACK key"""
        self.setMsg("Back")
        hist = self.history.get()
        if hist is not None:
            self.clear()
            self.currObject = hist
        else:
            lg.warning("Trying to go back, but history is empty!")

    def performHelp(self):
        """Enter help"""
        self.setCurrentObject(help())

    def followCurrent(self):
        """Fetches link  from current cmd and tries to follow it."""
        lg.debug("cli::followCurrent " +
                 str(self.currObject.currLine))
        link = self.currObject.getLink(self.currObject.currLine)

        c = comments(link.addr, rLimit=100)
        if c.ok:
            self.setCurrentObject(c)
        else:
            self.setCurrentObject(error(c.status))

        self.clear()

    def setCurrentObject(self, currObject):
        """
        Set current object, used for printing end evaluating commands.
        Arguments:
            currObject(rObject): reddit object
        """
        self.clear()
        if self.currObject is not None:
            self.history.add(self.currObject)
            self.history.update()
        self.currObject = currObject

    def setMsg(self, msg):
        """
        Set msg to show in status line
        Arguments:
            msg(string): text to show
        """
        self.msg = msg

    def clearMsg(self):
        """Clear msg to show in status line"""
        self.msg = None

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
