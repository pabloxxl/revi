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
            lg.debug("Removing oldest element from history list")
            self.history_list.pop()

    def add(self, currObject):
        """
        Add reddit object to history_list.
        Arguments:
            currObject(rObject): reddit object
        """
        lg.debug("history::add " + currObject.describe())
        self.history_list.append(currObject)

    def get(self):
        """ Get youngest element, remove it and return """
        lg.debug("history::get")
        if len(self.history_list) > 0:
            hist = self.history_list.pop()
            lg.debug("Poping from history " + hist.describe())
            return hist
        else:
            return None
