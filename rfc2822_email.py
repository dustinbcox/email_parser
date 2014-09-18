
""" Handle the dirty work of parsing the email """

import re
import datetime

MESSAGEID_REGEX = re.compile(r'(?P<message_id>^Message-ID: ?([\w@<>\.]*))')
FOLDING_REGEX = re.compile(r'^ +')
ENVELOPE_REGEX = \
    re.compile(r'^(?P<key>\w+): ?(?P<value>([\w<@> ;\.\?\\"\']+(?: *, *)?)+)')
DATE_REGEX = re.compile(r'^Date: ?(?P<day_name>(Mon|Tue|Wed|Thu|Fri|Sat|Sun))'+
                        r', (?P<day>\d+) (?P<month>(Jan|Feb|Mar|Apr|May|Jun|'+
                        r'Jul|Aug|Sep|Oct|Nov|Dec)) (?P<year>\d{4}) '+
                        r'(?P<hour>\d\d):(?P<min>\d\d):(?P<sec>\d\d) '+
                        r'(?P<tz>(\+|\-)\d{4})')


class Email(object):
    """Container & parser for an email"""
    def __init__(self, debug=False):
        self._header = {}
        self._body = ""
        self._debug = debug

    @property
    def from_address(self):
        """ From Address """
        return self._header['From']

    @property
    def to_address(self):
        """ To address """
        return self._header['To']

    @property
    def subject(self):
        """ Subject or None if undefined """
        if 'Subject' in self._header:
            return self._header['Subject']
        else:
            return None

    @property
    def date(self):
        """ Date """
        return self._header['Date']

    @property
    def message_id(self):
        """ Message-ID header """
        return self._header['message-id']

    @property
    def body(self):
        """ Entire body (without MIME) """
        return self._body
        

    def parse(self, full_email):
        """ Preform the actual paring of the full_email"""

        # States (in_header=True or False if in body)
        in_header = True
        # As per RFC folding is a line continuation
        is_folding = False
        last = None

        for line_num, line in enumerate(full_email.splitlines()):
            if self._debug:
                print("{0}:{1}".format(line_num, line))
            if in_header:
                if line == "":
                    # Marks the beginning of the body
                    in_header = False
                    continue
                if FOLDING_REGEX.search(line) is not None:
                    if last is not None:
                        self._header[last] += line
                        continue
                    else:
                        raise ValueError("Parse error! Expected previous " +
                                         "header before header folding on " +
                                         "line:" + str(line_num))
                parse = ENVELOPE_REGEX.search(line)
                if parse is not None:
                    parse = parse.groupdict()
                    self._header[parse['key']] = parse['value']
                    last = parse['key']
                    continue

                parse = MESSAGEID_REGEX.search(line)
                if parse is not None:
                    self._header['Message-ID'] = \
                                parse.groupdict()['message_id']
                    continue
                date = DATE_REGEX.search(line)
                if date is not None:
                    month_to_number = { month: num + 1 for num, month in
                                        enumerate(
                                            ('Jan','Feb','Mar','Apr','May',
                                             'Jun','Jul','Aug','Sep','Oct',
                                             'Nov','Dec'))}
                    date = date.groupdict()
                    self._header['Date'] = datetime.datetime(date['year'], 
                                            month_to_number[date['month']],
                                            date['day'],
                                            date['hour'],
                                            date['min'],
                                            date['sec'],
                                            tzinfo=date['tz'])

                if line.startswith('Subject:'):
                    # Simple line parsing
                    self._header['Subject'] = line.split(': ')[1]
 
            else: # In body
                self._body += line + "\r\n"
            
    def __str__(self):
        """Return just the basics of the email"""
        return "From:{0} To:{1} Subject:{2}".format(self.from_address,
                                                    self.to_address,
                                                    self.subject)
        
         
