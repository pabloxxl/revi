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
import logging as lg


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

        lg.debug("request::__init__ " +
                 self.rId)

        try:
            self.r = requests.get(self.rId, headers=USER_AGENT)
            self.status = self.r.status_code
        except requests.exceptions.RequestException as e:
            lg.error(e)
            self.status = 0

        if self.status is 200:
            self.ok = True
        else:
            self.ok = False
            lg.warning("Request returned " + str(self.status))

        if self.ok:
            self.json = self.r.json()

    def dump(self):
        """Dump request and all children"""
        lg.debug("request::dump")

        if self.ok:
            data = self.r.json()
            lg.debug("Dumping: " + self.rId)
            lg.debug(DD)
            lg.debug(data)
            lg.debug(DD)

            if "data" in data:
                for child in data['data']['children']:
                    lg.debug(child)
            else:
                lg.debug("Failed to dump data")

            lg.debug(DD)
        else:
            lg.debug("Return code:" + str(self.status))
