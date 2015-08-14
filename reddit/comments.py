from request import request
from rObject import rObject
from rObject import sortType
from rObject import typeStr

import logging as lg


class comment:
    def __init__(self, author, text):
        self.author = author
        self.text = text
        # lg.debug("link::__init__ " + author + " " + text[:25])


class comments(rObject):
    """
    Representation of reddit comments section
    Args:
        rLink (string): link to comment section
        rType (optional[sortType]): how to sort results. Defaults sortType.HOT
        rLimit (optional[int]): ammount of fetched comments. Defaults 25
    """
    def __init__(self, rLink, rType=sortType.HOT, rLimit=25):
        rTypeTxt = typeStr(rType)
        lg.debug("comments::__init__ " +
                 rLink + "" +
                 rTypeTxt + " " +
                 str(rLimit))

        self.currComment = 0

        self.r = request(rLink, None)
        # I should check if request went well

        self.json = self.r.json
        self.__fetchComments__()

    def decrement(self):
        """Decrease current comment"""
        if self.currComment > 0:
            lg.debug("comments::decrement %d -> %d",
                     self.currComment,
                     self.currComment - 1)
            self.currComment -= 1
        else:
            lg.debug("comments::decrement %d -> MIN",
                     self.currComment)

    def increment(self):
        """Increase current line"""
        if self.currComment < len(self.comments) - 1:
            lg.debug("comments::increment %d -> %d",
                     self.currComment,
                     self.currComment + 1)
            self.currComment += 1
        else:
            lg.debug("comments::increment %d -> MAX",
                     self.currComment)
            self.currComment += 1

    def top(self):
        """Set current line to 0"""
        lg.debug("comments::top %d -> %d",
                 self.currComment,
                 0)

        self.currComment = 0

    def bottom(self):
        """Set current line to max"""

        lg.debug("comments::bottom %d -> %d",
                 self.currComment,
                 len(self.comments) - 1)

        self.currComment = len(self.comments) - 1

    def dump(self):
        """Dump request object"""
        lg.debug("comments::dump")
        self.r.dump()

    def __fetchComments__(self):
        lg.debug("comments::__fetchComments")

        self.comments = []
        for child in self.json[1]['data']['children']:
            if child['kind'] == 't1':
                c = comment(child['data']['author'], child['data']['body'])
                self.comments.append(c)
