DEBUG = True
from request import request


class user:
    def __init__(self, uName):
        if DEBUG:
            print "user::__init__"
            print "\t"+uName

        rTxtOverview = 'user/'+uName+'/overview/'
        self.rOverview = request(rTxtOverview)

    def dump(self):
        self.rOverview.dump()
