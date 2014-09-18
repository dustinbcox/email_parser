#!/usr/bin/env python2.7

"""
Simple Email parser
"""

import argparse

import sys
import os

# Insert top level project dir
#sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rfc2822_email import Email

def read_email_from_file(filename):
    """ Open a filename and read the entire contents into memory """
    with open(filename, 'r') as filehandle:
        data = filehandle.read()
    return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Simple RFC2822 Email parser")
    parser.add_argument('--debug', action='store_true', help="Enable debugging")
    parser.add_argument('file', nargs='+', help="File to parse")
    args = parser.parse_args()
    if args.debug:
        print("DEBUG mode enabled")

    for filename in args.file:
        if args.debug:
            print("Parse :" + filename)
        email = Email(debug=args.debug)
        email.parse(read_email_from_file(filename))
        print email
