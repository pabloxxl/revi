from request import request
from rObject import rObject
from rObject import sortType
from rObject import typeStr

import logging as lg


class link:
    def __init__(self, title, addr):
        self.title = title
        self.addr = addr
        # lg.debug("link::__init__ "+title[:10].encode('utf8')+"...")


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
        lg.debug("listing::__init__ " +
                 rTypeTxt + " " +
                 str(rLimit))

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
        lg.debug("listing::getLink " +
                 str(number))
        return self.links[number]

    def decrement(self):
        """Decrease current line"""
        if self.currLine > 0:
            lg.debug("listing::decrement %d -> %d",
                     self.currLine,
                     self.currLine - 1)
            self.currLine -= 1
        else:
            lg.debug("listing::decrement %d -> MIN",
                     self.currLine)

    def increment(self):
        """Increase current line"""
        if self.currLine < len(self.links) - 1:
            lg.debug("listing::increment %d -> %d",
                     self.currLine,
                     self.currLine + 1)
            self.currLine += 1
        else:
            lg.debug("listing::increment %d -> MAX",
                     self.currLine)

    def top(self):
        """Set current line to 0"""
        lg.debug("listing::top %d -> %d",
                 self.currLine,
                 0)

        self.currLine = 0

    def bottom(self):
        """Set current line to max"""

        lg.debug("listing::bottom %d -> %d",
                 self.currLine,
                 len(self.links) - 1)

        self.currLine = len(self.links) - 1

    def dump(self):
        """Dump request object"""
        lg.debug("listing::dump")
        self.r.dump()

    def __fetchLinks__(self):
        lg.debug("listing::__fetchLinks")

        self.links = []
        for child in self.json['data']['children']:
            l = link(child['data']['title'], child['data']['permalink'])
            self.links.append(l)
