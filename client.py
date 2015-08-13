#!/usr/bin/env python

from cli import window
import argparse

VERSION = "0.1"

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

# Run main loop
if args.cli:
    w = window()
    w.run()
    print "TERMINATED"
else:
    print "GTK version is not supported yet"
