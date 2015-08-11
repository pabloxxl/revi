DEBUG = False
"""Debug printouts in every function"""
PREFIX = "http://www.reddit.com"
"""Common request prefix"""
SUFIX = ".json"
"""Common request suffix"""
DD = "===================="
"""Delimiter, used in dumps"""

USER_AGENT = {'User-agent': 'revi:v0.1 (by /u/pabloxxl)'}
"""User agent. According to reddit api guide, it should be unique"""
# TODO add version id
import requests


class request:
    """
    Representation of reddit api request
    Args:
        rTxt (string): middle part of url (stripped of PREFIX and SUFIX)
        rParams (optional[string]): optional parameters (appended after ?)
    TODO: list of error codes
    """
    def __init__(self, rTxt, rParams=None):
        self.rId = PREFIX + rTxt + SUFIX
        # TODO add cutting prefix end sufix

        if rParams is not None:
            self.rId += "?"+rParams

        if DEBUG:
            print "request::__init__"
            print "\t"+self.rId

        # TODO add error handling
        self.r = requests.get(self.rId, headers=USER_AGENT)

        self.json = self.r.json()

    def dump(self):
        """Dump request and all children"""
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
