DEBUG = False
"""Debug printouts in every function"""
from request import request
from rObject import rObject
from rObject import sortType
from rObject import typeStr


class comment:
    def __init__(self, author, text):
        self.author = author
        self.text = text
        if DEBUG:
            print "[[link::__init__ " + author + " " + text[:25]


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
        if DEBUG:
            print "comments::__init__"
            print "\t"+str(rLink)
            print "\t"+str(rTypeTxt)
            print "\t"+str(rLimit)

        self.currComment = 0

        self.r = request(rLink, None)
        # I should check if request went well

        self.json = self.r.json
        self.__fetchComments__()

    def decrement(self):
        """Decrease current comment"""
        if self.currComment > 0:
            self.currComment -= 1

    def increment(self):
        """Increase current comment"""
        if self.currComment < len(self.comments) - 1:
            self.currComment += 1

    def top(self):
        """Set current comment to 0"""
        self.currComment = 0

    def bottom(self):
        """Set current comment to max"""
        self.currComment = len(self.comments) - 1

    def dump(self):
        """Dump request object"""
        self.r.dump()

    def __fetchComments__(self):
        if DEBUG:
            print "listing::__fetchComments"

        self.comments = []
        for child in self.json[1]['data']['children']:
            if child['kind'] == 't1':
                c = comment(child['data']['author'], child['data']['body'])
                self.comments.append(c)
