import curses


class cmd:
    """ Commands, returned to cli.py as response for text"""
    QUIT = 0
    SWITCH_TO_NORMAL = 1
    SWITCH_TO_COMMAND = 2
    SWITCH_TO_INSERT = 3
    DOWN = 21
    UP = 22


class mode:
    """This imitates vi modes, except visual and visual-block"""
    NORMAL, COMMAND, INSERT = range(3)


class eval_vim(object):
    """
    Responsible for evaluation of user pressed input.
    It tries to emulate VIM key commands.
    eval() method should be called in infinite loop.
    Arguments:
        stdscr(stdscr): instance of curses window
    """
    def __init__(self, stdscr):
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
        if text == "q":
            return cmd.QUIT
        elif text == "quit":
            return cmd.QUIT
        else:
            return cmd.SWITCH_TO_NORMAL

    def __evalNormal__(self, char, prevChar):
        """
        Evaluate char (and preceding char) used in normal mode
        Arguments:
            char(string): pressed key
            prevChar(string): previously pressed key
        Returns:
            (cmd): command object. None if no command was found
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
        else:
            return None

    def eval(self):
        """
        Evaluate key pressed by user, and process it according to MODE
        Returns:
            (cmd): command object
        """
        val = None
        # Gather input
        if self.mode is mode.NORMAL:
            self.prevChar = self.char
            self.char = self.stdscr.getch()

            val = self.__evalNormal__(chr(self.char), chr(self.prevChar))
            if val is not None:
                self.reset()
            return val

        elif self.mode is mode.COMMAND:
            self.char = self.stdscr.getch()
            if self.char is curses.KEY_ENTER or self.char is ord("\n"):
                val = self.cmd = self.__evalCommand__(self.text)
                self.reset()
            else:
                self.text += chr(self.char)
            return val

    def reset(self):
        """Resets all stored values"""
        self.char = 0
        self.prevChar = 0
        self.text = ""
