DEBUG = True
from request import request


class sortType:
    HOT, NEW, RISING, CONTROVERSIAL, TOP, GILDED, WIKI, PROMOTED = range(8)


def typeStr(type):
    if type is sortType.HOT:
        return "hot"
    elif type is sortType.RISING:
        return "rising"
    elif type is sortType.CONTROVERSIAL:
        return "controversial"
    elif type is sortType.TOP:
        return "top"
    elif type is sortType.GILDED:
        return "gilded"
    elif type is sortType.WIKI:
        return "wiki"
    elif type is sortType.PROMOTED:
        return "promoted"
    else:
        return ""


class listing:
    def __init__(self, rName, rType=sortType.HOT, rLimit=25):
        rTypeTxt = typeStr(rType)
        if DEBUG:
            print "listing::__init__"
            print "\t"+str(rTypeTxt)
            print "\t"+str(rLimit)

        rLimitTxt = None
        if rLimit is not 25:
            rLimitTxt = "limit="+str(rLimit)
        # TODO add other options

        rTxt = 'r/'+rName+'/'+rTypeTxt+'/'

        params = rLimitTxt
        # add other options to params

        self.r = request(rTxt, params)
        # I should check if request went well

        self.json = self.r.json
        self.__fetchLinks__()

    def dump(self):
        self.r.dump()

    def __fetchLinks__(self):
        if DEBUG:
            print "listing::__fetchLinks"

        self.links = []
        for child in self.json['data']['children']:
            self.links.append(child['data']['title'])
