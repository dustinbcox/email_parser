"""
Provide unit testing for email parser
"""

import unittest
import logging
import os.path
import sys
import json
import glob

def setup_log():
    """ Setup logging to console """
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    log_stream = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    log_stream.setFormatter(formatter)
    log.addHandler(log_stream)
    return log

#
# Convenient Globals

#
LOG = setup_log()
CWD = os.path.dirname(os.path.abspath(__file__))

# Insert parent dir into PYTHONPATH
sys.path.insert(0, os.path.join(CWD, ".."))

# Module to test
from rfc2822_email import Email
from email_parse import read_email_from_file

# Unit testing
class EmailTest(unittest.TestCase):
    def setUp(self):
        """ Read in all sample(s) """
        self._emails = {}
        os.chdir(CWD)
        for filename in glob.glob('raw_email_??.txt'):
            self._emails[filename] = read_email_from_file(filename)

    def test_email(self):
        """ Test parsing content """
        for email, content in self._emails.items():
            expected = json.loads(read_email_from_file(
                                    email.replace(".txt", ".json")))
            email_parser = Email()
            email_parser.parse(content)
            self.assertEquals(expected['To'], email_parser.to_address)
            self.assertEquals(expected['From'], email_parser.from_address)


