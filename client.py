#!/usr/bin/env python

from cli import window
import argparse
import time
import logging as lg
import ConfigParser
import os
import sys

VERSION = "0.1"
LOGNAME = "revi.log"
CONFIG = "~/.revirc"


def parse():
    """
    Parse commandline options
    Return:
        (namespace): options
    """
    parser = argparse.ArgumentParser(description="revi v"+VERSION,
                                     epilog="developed by Pawel Cendrzak")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-g", "--gtk", action="store_true",
                       help="use cli mode (ncurses)")
    group.add_argument("-c", "--cli", action="store_true",
                       help="use graphical mode (GTK)")
    parser.add_argument("-d", "--debug",
                        help="enter debug mode",
                        action="store_true")

    return parser.parse_args()


def setLogger(debug):
    """Setup logger module
    Arguments:
        debug(bool): Should debug printouts be visible
    """
    # Remove old log file
    if os.path.isfile(LOGNAME):
      os.remove(LOGNAME)

    f='[%(levelname)s] %(module)s::%(funcName)s:%(lineno)s %(message)s'

    if debug:
      lg.basicConfig(format='[%(levelname)s][%(asctime)s] %(module)s::%(funcName)s:%(lineno)s %(message)s',
                       level=lg.DEBUG,
                       filename=LOGNAME)

    else:
      lg.basicConfig(format='[%(levelname)s][%(asctime)s] %(message)s',
                       level=lg.INFO,
                       filename=LOGNAME)

    # Do not print requests module logs
    lg.getLogger("requests").setLevel(lg.WARNING)

    lg.info("revi v%d", VERSION)
    lg.info(time.strftime("Log started at %H:%M:%S (%d.%m.%Y)"))


def readConfig():
    """
    Read config file.
    Return:
        (dict): Parsed options
    """
    cd = {}
    config = ConfigParser.ConfigParser()
    ret = config.read(os.path.expanduser(CONFIG))

    # Read system specific options
    if sys.platform == "darwin":
        lg.info("OS X detected. Setting browser: safari")
        cd["browser"] = "open -a safari"
    else:
        lg.info("Unknown system version")

    # Check if config file was found
    if len(ret) is 0:
        lg.warning("Config file not found!")
        return cd

    if config.has_option(None, "user"):
        cd['user'] = config.get("DEFAULT", "user")
        lg.info("cd[user]: %s", cd['user'])

    if config.has_option(None, "history_max"):
        cd['history_max'] = config.get("DEFAULT", "history_max")
        lg.info("cd[history_max]: %s", cd['history_max'])

    return cd

if __name__ == "__main__":
    # Run main loop
    args = parse()
    setLogger(args.debug)
    config = readConfig()
    if config is None:
        print ".revirc not found. Assuming defaults"

    if args.cli:
        w = window(config)
        w.run()
        print "Revi finished normally"
    else:
        lg.error("GTK version is not supported yet. Exiting")
        print "GTK version is not supported yet"
else:
    print "Library mode is not implemented"
