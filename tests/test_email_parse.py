"""
Provide unit testing for email parser
"""

import unittest
import logging
import os.path
import sys

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

import email_parse


class MainTest(unittest.TestCase):
    def setUp(self):
        """ Read in all sample(s) """
        samples = ['raw_email_01.txt']
        self._samples = []

        for sample in samples:
            LOG.info("Reading email file: " + sample)
            sample_path = os.path.join(CWD, sample)
            with open(sample_path, "r") as sample_email_file:
                self._samples.append(sample_email_file.read())

    def test_foo(self):
        print self._samples
