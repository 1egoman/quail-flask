from datetime import datetime
from json import loads
import os

DEFAULTCONFIG = """[]"""

class Calender(object):

  def __init__(self, app):
    self.events = []
    cfgpath = os.path.join(app.get_root(), "config", "events.json")

    # see if config exists
    if not os.path.exists(cfgpath):
      with open( cfgpath, 'w' ) as f:
        f.write(DEFAULTCONFIG)

    with open( cfgpath, 'r' ) as f:
      self.events = loads( f.read() )

  def add_event(self, name, when, where=None):
    """ Add a new event to the calender """
    event = {}
    event["name"] = name
    event["when"] = when
    event["where"] = where
    self.events.append(event)

    self.sync()

  def sync(self):
    """ Sync the file and the program's list """
    with open( cfgpath, 'w' ) as f:
      f.write( dumps(self.events, indent=2) )
