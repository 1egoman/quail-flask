from datetime import datetime
from json import loads, dumps
import os

DEFAULTCONFIG = """[]"""

class Calender(object):

  def __init__(self, app):
    self.events = EventList()
    self.cfgpath = os.path.join(app.get_root(), "config", "events.json")

    # see if config exists
    if not os.path.exists(self.cfgpath):
      with open( self.cfgpath, 'w' ) as f:
        f.write(DEFAULTCONFIG)

    # read config
    with open( self.cfgpath, 'r' ) as f:
      r = f.read()
      if len(r): 
        self.events = EventList( loads( r ) )

  def add_event(self, name, when, where=None, **kwargs):
    """ Add a new event to the calender """
    event = {}
    event["name"] = name
    event["when"] = when and when.strftime('%c')
    event["where"] = where
    event.update(kwargs)
    self.events.append(event)

    self.sync()


  def sync(self):
    """ Sync the file and the program's list """
    with open( self.cfgpath, 'w' ) as f:
      f.write( dumps(self.events, indent=2) )

  def as_html(self):
    pass

  def where(self, name=None, when=None, where=None):
    gooditems = []
    for e in self.events:
      gn = 0
      if (not name) or (name and e["name"] == name):
        gn = 1
      gwh = 0
      if (not where) or (where and e["where"] == where):
        gwh = 1
      gwn = 0
      if (not when) or (when and e["when"] == when):
        gwn = 1

      if gn and gwh and gwn:
        gooditems.append(e)

    return gooditems


class EventList(list):
  """ A list that holds events """

  def year(self, year):
    """ Get all events where year = 'year' """
    return EventList([e for e in self if datetime.strptime(e["when"], '%c').strftime('%Y') == str(year)])

  def month(self, month):
    """ Get all events where month = 'month' """
    if type(month) == int:
      return EventList([e for e in self if int(datetime.strptime(e["when"], '%c').strftime('%m')) == month])
    else:
      return EventList([e for e in self if datetime.strptime(e["when"], '%c').strftime('%B') == str(month) or datetime.strptime(e["when"], '%c').strftime('%b') == str(month)])

  def day(self, day):
    """ Get all events where day = 'day' """
    return EventList([e for e in self if int(datetime.strptime(e["when"], '%c').strftime('%d')) == int(day)])

  def week(self, week):
    """ Get all events where week = 'week' """
    return EventList([e for e in self if int(datetime.strptime(e["when"], '%c').strftime('%W')) == int(week)])