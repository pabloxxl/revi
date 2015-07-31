DEBUG = True
from request import request


class user(request):
    def __init__(self, uName):
        if DEBUG:
            print "user::__init__ : " + uName

        rTxt = 'user/'+uName+'/overview/'
        request.__init__(self, rTxt)
