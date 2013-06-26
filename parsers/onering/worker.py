import time
import re

from logster.logster_helper import MetricObject, LogsterParser
from logster.logster_helper import LogsterParsingException

class Worker(LogsterParser):

  def __init__(self, option_string=None):
    self.observations = []
    self.times = re.compile('^(?P<action>(?:Starting|Finished)) job (?P<job>[\w\-]+) .*\((?:(?:took (?P<ttf>[\d\.]+) seconds)|(?:(?P<tts>[\d\.]+) seconds ago))\).*')


  def parse_line(self, line):
    '''This function should digest the contents of one line at a time, updating
    object's state variables. Takes a single argument, the line to be parsed.'''

    try:
      # Apply regular expression to each line and extract interesting bits.
      regMatch = self.times.match(line)

      if regMatch:
        linebits = regMatch.groupdict()
        self.observations.append({
          job:           linebits['job'],
          time_queued:   float(linebits['tts'] or 0.0),
          time_running:  float(linebits['ttf'] or 0.0)
        })

      else:
        raise LogsterParsingException, "regmatch failed to match"

    except Exception, e:
      raise LogsterParsingException, "regmatch or contents failed with %s" % e


  def get_state(self, duration):
    rv = []

    for o in self.observations:
      if o['time_queued'] > 0.0:
        rv.append(MetricObject(o['job'].lower()+'.time_queued', o['time_queued'], "Seconds"))

      if o['time_running'] > 0.0:
        rv.append(MetricObject(o['job'].lower()+'.time_running', o['time_running'], "Seconds"))

    return rv
