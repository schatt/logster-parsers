import time
import re

from logster.logster_helper import MetricObject, LogsterParser
from logster.logster_helper import LogsterParsingException

class DHCP(LogsterParser):

  def __init__(self, option_string=None):
    self.metrics = {}
    self.dhcp_types = ['DISCOVER', 'OFFER', 'REQUEST', 'ACK', 'NACK']

  # initialize to zero
    for t in self.dhcp_types:
      self.metrics[t] = 0

    self.reg = re.compile('.*dnsmasq-dhcp.*: DHCP(?P<type>(?:' + '|'.join(self.dhcp_types) + ')).*')


  def parse_line(self, line):
    '''This function should digest the contents of one line at a time, updating
    object's state variables. Takes a single argument, the line to be parsed.'''

    try:
      # Apply regular expression to each line and extract interesting bits.
      regMatch = self.reg.match(line)

      if regMatch:
        linebits = regMatch.groupdict()
        dhcp_type = linebits['type']
   
        if dhcp_type in self.dhcp_types:
          self.metrics[dhcp_type] += 1

      else:
        raise LogsterParsingException, "regmatch failed to match"

    except Exception, e:
      raise LogsterParsingException, "regmatch or contents failed with %s" % e


  def get_state(self, duration):
    rv = []
    
    for t in self.dhcp_types:
      rv.append(MetricObject(t.lower(), self.metrics[t], "Count"))

    return rv
