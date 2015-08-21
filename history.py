import logging as lg

HISTORY_COUNT = 5  # Read it from config


class history:
    """
    Holder of history - last used reddit objects
    """
    def __init__(self):
        lg.debug("history::__init__")
        self.history_list = []

    def update(self):
        """
        Check if length of history_list is bigger than HISTORY_COUNT.
        If so, remove oldest element
        """
        lg.debug("history::update")
        if len(self.history_list) > HISTORY_COUNT:
            self.history_list.pop()

    def add(self, currObject):
        """
        Add reddit object to history_list.
        Arguments:
            currObject(rObject): reddit object
        """
        lg.debug("history::add " + currObject.describe())
