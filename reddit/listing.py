from request import request
from rObject import rObject
from rObject import sortType
from rObject import typeStr

import logging as lg


class link:
    def __init__(self, title, addr):
        self.title = title
        self.addr = addr
        self.url = None


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
        lg.debug("%s %d", rTypeTxt, rLimit)

        self.rName = rName
        self.rType = rType

        if self.rName == "":
            self.rName = "front"

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

        self.ok = self.r.ok
        self.status = self.r.status

        if self.ok:
            self.json = self.r.json
            self.__fetchLinks__()

    def getLink(self, number):
        """Return link at specifed position"""
        lg.debug("%d", number)
        return self.links[number]

    def decrement(self):
        """Decrease current line"""
        if self.currLine > 0:
            lg.debug("%d -> %d",
                     self.currLine,
                     self.currLine - 1)
            self.currLine -= 1
        else:
            lg.debug("%d -> MIN", self.currLine)

    def increment(self):
        """Increase current line"""
        if self.currLine < len(self.links) - 1:
            lg.debug("%d -> %d",
                     self.currLine,
                     self.currLine + 1)
            self.currLine += 1
        else:
            lg.debug("%d -> MAX",
                     self.currLine)

    def top(self):
        """Set current line to 0"""
        lg.debug("%d -> %d",
                 self.currLine,
                 0)

        self.currLine = 0

    def bottom(self):
        """Set current line to max"""

        lg.debug("%d -> %d",
                 self.currLine,
                 len(self.links) - 1)

        self.currLine = len(self.links) - 1

    def describe(self):
        """Print listing description"""
        return "LISTING: " + self.rName + "(" + typeStr(self.rType) + ")"

    def dump(self):
        """Dump request object"""
        lg.debug("")
        self.r.dump()

    def __fetchLinks__(self):
        lg.debug("")

        self.links = []
        for child in self.json['data']['children']:
            l = link(child['data']['title'], child['data']['permalink'])
            l.url = child['data'].get("url", None)
            self.links.append(l)
