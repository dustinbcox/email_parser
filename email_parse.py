#!/usr/bin/env python2.7

"""
Simple Email parser
"""

import argparse
import re



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Email parser")
    parser.add_argument('--debug', action='store_true', help="Enable debugging")
    args = parser.parse_args()
    if args.debug:
        print "DEBUG"
    print "DO nothing"
