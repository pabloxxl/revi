#!/usr/bin/env python

from cli import window
import argparse
import time
import logging

VERSION = "0.1"
LOGNAME = "revi.log"

# Parse program arguments
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

args = parser.parse_args()
if args.debug:
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.DEBUG,
                        filename=LOGNAME)

else:
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.INFO,
                        filename=LOGNAME)

logging.getLogger("requests").setLevel(logging.WARNING)

logging.info("revi v"+VERSION)
logging.info(time.strftime("Log started at %H:%M:%S (%d.%m.%Y)"))


# Run main loop
if args.cli:
    w = window()
    w.run()
    print "TERMINATED"
else:
    print "GTK version is not supported yet"
