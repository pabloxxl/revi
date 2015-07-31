DEBUG = True
PREFIX = "http://www.reddit.com/"
SUFIX = ".json"
DD = "===================="

USER_AGENT = {'User-agent': 'revi:v0.1 (by /u/pabloxxl)'}
# TODO add version id
import requests


class request:
    def __init__(self, rTxt):
        self.rId = PREFIX + rTxt + SUFIX
        # TODO add cutting prefix end sufix

        if DEBUG:
            print "request::__init__ : " + self.rId

        # TODO add error handling
        self.r = requests.get(self.rId, headers=USER_AGENT)

    def getJson(self):
        return self.r.json()

    def dump(self):
        data = self.r.json()
        print "Dumping: " + self.rId
        print DD
        print data
        print DD

        if "data" in data:
            for child in data['data']['children']:
                print child
        else:
            print "Failed to dump data"

        print DD
