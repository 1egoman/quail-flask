from datetime import datetime
from json import loads, dumps
import os

DEFAULTCONFIG = """{"people": []}"""
PERSONTEMPLATE = {"name": None, "tags": None, "birthday": None, "pic": None, "frequency": 0}

class PeopleContainer(object):

  def __init__(self, app):
    self.data = []
    self.cfgpath = os.path.join(app.get_root(), "config", "people.json")

    # see if config exists
    if not os.path.exists(self.cfgpath):
      with open( self.cfgpath, 'w' ) as f:
        f.write(DEFAULTCONFIG)

    # read config
    with open( self.cfgpath, 'r' ) as f:
      r = f.read()
      if len(r): 
        self.data = loads( r )["people"]
      else:
        self.data = []

  def sync(self):
    """ Sync the file and the program's list """
    with open( self.cfgpath, 'w' ) as f:
      f.write( dumps({"people": self.data}, indent=2) )

  def add_person(self, **person):
    """ Add a new person to the list of known people """
    person = PERSONTEMPLATE.copy().update(person)
    self.data.append(person)