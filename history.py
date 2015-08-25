import logging as lg


class history:
    """
    Holder of history - last used reddit objects
    Arguments:
        max(int): maximum ammount of saved history
    """
    def __init__(self, max):
        lg.debug("history::__init__ " + str(max))
        self.max = max
        self.history_list = []

    def update(self):
        """
        Check if length of history_list is bigger than max.
        If so, remove oldest element
        """
        lg.debug("history::update")
        if len(self.history_list) > max:
            self.history_list.pop()

    def add(self, currObject):
        """
        Add reddit object to history_list.
        Arguments:
            currObject(rObject): reddit object
        """
        lg.debug("history::add " + currObject.describe())
