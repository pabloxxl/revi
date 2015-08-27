#!/usr/bin/env python

from cli import window
import argparse
import time
import logging
import ConfigParser
import os

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
    if debug:
        logging.basicConfig(format='%(levelname)s:%(message)s',
                            level=logging.DEBUG,
                            filename=LOGNAME)

    else:
        logging.basicConfig(format='%(levelname)s:%(message)s',
                            level=logging.INFO,
                            filename=LOGNAME)

    # Do not print requests module logs
    logging.getLogger("requests").setLevel(logging.WARNING)

    logging.info("revi v"+VERSION)
    logging.info(time.strftime("Log started at %H:%M:%S (%d.%m.%Y)"))


def readConfig():
    """
    Read config file.
    Return:
        (dict): Parsed options
    """
    config = ConfigParser.ConfigParser()
    ret = config.read(os.path.expanduser(CONFIG))
    if len(ret) is 0:
        return {}
    cd = {}
    if config.has_option(None, "user"):
        cd['user'] = config.get("DEFAULT", "user")
    # Worst idea EVER
    if config.has_option(None, "password"):
        cd['password'] = config.get("DEFAULT", "password")

    if config.has_option(None, "history_max"):
        cd['history_max'] = config.get("DEFAULT", "history_max")
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
        print "GTK version is not supported yet"
else:
    print "Library mode is not implemented"
