import time
import re

from logster.logster_helper import MetricObject, LogsterParser
from logster.logster_helper import LogsterParsingException

class Worker(LogsterParser):

  def __init__(self, option_string=None):
    self.observations = []
    self.job_counts = {}
    self.times = re.compile('^(?P<action>(?:Starting|Finished)) job (?P<job>[\w\-]+) .*\((?:(?:took (?P<ttf>[\d\.]+) seconds)|(?:(?P<tts>[\d\.]+) seconds ago))\).*')


  def parse_line(self, line):
    '''This function should digest the contents of one line at a time, updating
    object's state variables. Takes a single argument, the line to be parsed.'''

    try:
    # Apply regular expression to each line and extract interesting bits.
      regMatch = self.times.match(line)

      if regMatch:
        linebits = regMatch.groupdict()

        if linebits.get('job'):
        # save parsed results
          self.observations.append({
            'job':          linebits['job'],
            'time_queued':  float(linebits.get('tts') or 0.0),
            'time_running': float(linebits.get('ttf') or 0.0)
          })

        # create if not exist
          if not linebits['job'] in self.job_counts:
            self.job_counts[linebits['job']] = 0

        # increment counter
          self.job_counts[linebits['job']] = self.job_counts[linebits['job']] + 1

      else:
        pass

    except Exception, e:
      raise LogsterParsingException, "regmatch or contents failed with %s" % e


  def get_state(self, duration):
    rv = []

  # return times
    for o in self.observations:
      if o['time_queued'] > 0.0:
        rv.append(MetricObject(o['job'].lower()+'.time_queued', o['time_queued'], "Seconds"))

      if o['time_running'] > 0.0:
        rv.append(MetricObject(o['job'].lower()+'.time_running', o['time_running'], "Seconds"))

  # return counters
    for name, count in self.job_counts.items():
      rv.append(MetricObject(name.lower()+'.count', count, "Count"))

    return rv
