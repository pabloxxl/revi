DEBUG = False
"""Debug printouts in every function"""
from request import request
from rObject import rObject
from rObject import sortType
from rObject import typeStr


class link:
    def __init__(self, title, addr):
        self.title = title
        self.addr = addr
        if DEBUG:
            print "[[link::__init__ "+title.encode('utf8')+"]]"


class listing(rObject):
    """
    Representation of reddit listing (list of links in subredit)
    Args:
        rName (string): subredit name
        rType (optional[sortType]): how to sort results. Defaults sortType.HOT
        rLimit (optional[int]): ammount of fetched links. Defaults 25
    """
    def __init__(self, rName, rType=sortType.HOT, rLimit=25):
        rTypeTxt = typeStr(rType)
        if DEBUG:
            print "listing::__init__"
            print "\t"+str(rTypeTxt)
            print "\t"+str(rLimit)

        self.currLine = 0
        rLimitTxt = None
        if rLimit is not 25:
            rLimitTxt = "limit="+str(rLimit)
        # TODO add other options
        if rName is "":
            rTxt = "/"
        else:
            rTxt = '/r/'+rName+'/'+rTypeTxt+'/'

        params = rLimitTxt
        # add other options to params

        self.r = request(rTxt, params)
        # I should check if request went well

        self.json = self.r.json
        self.__fetchLinks__()

    def getLink(self, number):
        """Return link at specifed position"""
        return self.links[number]

    def decrement(self):
        """Decrease current line"""
        if self.currLine > 0:
            self.currLine -= 1

    def increment(self):
        """Increase current line"""
        if self.currLine < len(self.links) - 1:
            self.currLine += 1

    def top(self):
        """Set current line to 0"""
        self.currLine = 0

    def bottom(self):
        """Set current line to max"""
        self.currLine = len(self.links) - 1

    def dump(self):
        """Dump request object"""
        self.r.dump()

    def __fetchLinks__(self):
        if DEBUG:
            print "listing::__fetchLinks"

        self.links = []
        for child in self.json['data']['children']:
            l = link(child['data']['title'], child['data']['permalink'])
            self.links.append(l)
