from eval import eval
from eval import cmd
import logging as lg


mapping_normal = {
    ":": cmd.SWITCH_TO_COMMAND,
    "i": cmd.SWITCH_TO_INSERT,
    "j": cmd.DOWN,
    "k": cmd.UP,
    "b": cmd.BACK,
    "B": cmd.BACK_ABSOLUTE,
    "G": cmd.BOTTOM,
    "ZZ": cmd.QUIT,
    "gg": cmd.TOP,
    "\n": cmd.ENTER
}

mapping_command = {
    "q": cmd.QUIT,
    "h": cmd.HELP,
    "quit": cmd.QUIT,
    "help": cmd.HELP,
    "license": cmd.LICENSE,
    "history": cmd.HISTORY
}


class mode:
    """This imitates vi modes, except visual and visual-block"""
    NORMAL, COMMAND, INSERT = range(3)


class eval_vim(eval):
    """
    Responsible for evaluation of user pressed input.
    It tries to emulate VIM key commands.
    eval() method should be called in infinite loop.
    Arguments:
        stdscr(stdscr): instance of curses window
    """
    def __init__(self, stdscr):
        lg.debug("eval_vim::__init__")
        self.mode = mode.NORMAL
        self.reset()
        self.stdscr = stdscr

    def __evalCommand__(self, text):
        """
        Evaluate command (string) stated in normal mode
        Arguments:
            text(string): text stated after ":" sign
        Returns:
            (cmd): command object. SWITCH_TO_NORMAL if no command was found
        """
        lg.debug("eval_vim::__evalCommand__ " +
                 text)

        self.mode = mode.NORMAL
        return mapping_command.get(text, cmd.SWITCH_TO_NORMAL)

    def __evalNormal__(self, char, prevChar):
        """
        Evaluate char (and preceding char) used in normal mode
        Arguments:
            char(string): pressed key
            prevChar(string): previously pressed key
        Returns:
            (cmd): command object. None if no command was found
        """
        lg.debug("eval_vim::__evalNormal__ " +
                 prevChar + char)

        if char is ':':
            self.mode = mode.COMMAND

        cmd = mapping_normal.get(char, None)
        if cmd is None:
            cmd = mapping_normal.get(prevChar + char)
        return cmd

    def eval(self):
        """
        Evaluate key pressed by user, and process it according to MODE
        Returns:
            (cmd): command object
        """
        lg.debug("eval_vim::eval")
        val = None
        # Gather input
        if self.mode is mode.NORMAL:
            self.prevChar = self.char
            self.char = self.stdscr.getkey()

            val = self.__evalNormal__(self.char, self.prevChar)
            if val is not None:
                self.reset()
            return val

        elif self.mode is mode.COMMAND:
            self.char = self.stdscr.getkey()
            if self.char == "\n":
                val = self.cmd = self.__evalCommand__(self.text)
                self.reset()
            else:
                self.text += self.char
            return val

    def reset(self):
        """Resets all stored values"""
        lg.debug("eval_vim::reset")
        self.char = ''
        self.prevChar = ''
        self.text = ""

    def draw(self, maxY, maxX):
        """
        Container method to all draw methods defined in eval class
        Arguments:
            maxY(int): window height
            maxX(int): windows width
        """
        lg.debug("eval_vim::draw")
        self.__drawFooter__(maxY, maxX)

    def __drawFooter__(self, maxY, maxX):
        """
        Draw menu on the bottom of screen
        It is managed here since only eval_vim know about current mode
        """
        lg.debug("eval_vim::__drawFooter__")
        if self.mode is mode.COMMAND:
            self.stdscr.addstr(maxY-1, 0, ":"+self.text)
        elif self.mode is mode.NORMAL:
            self.stdscr.addstr(maxY-1, 0,  " "*(maxX - 1))
