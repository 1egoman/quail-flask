from plugin import Plugin
from network import STATUS_OK
import datetime as dt

CAL_ADD_WORDS = ["named", "called", "create", "add"]
CAL_DEL_WORDS = ["named", "called", "check", "delete", "remove"]
STRIP_WORDS = ["to", "from", "on", "in", "by", "list"]
WHEN_WORDS = ["at", "for"]

class aPlugin(Plugin): pass

class CalPlugin(Plugin):

  def validate(self):
    return "calender" in self.query or "event" in self.query.as_str()

  def parse(self):

    # add
    if len([1 for t in CAL_ADD_WORDS if t in self.query]):

      # get when
      time = None
      when = [w for w in self.query if type(w) == dict and w["type"] == "time"]
      if len(when):
        time = dt.datetime.strptime(when[0]["when"], '%c')
      
      # get name
      start = None
      name = ""
      for ct,r in enumerate(self.query):

        if r in CAL_ADD_WORDS:
          start = ct+1

        elif start != None and r in STRIP_WORDS:
          name = ' '.join(self.query[start:ct])
          break

      # add it
      self.app.calender.add_event(name=name, when=time)

      self.resp["status"] = STATUS_OK
      self.resp["text"] = "Added %s to %s" % ( name, time.strftime("%A, %B %d, %Y") )

    # delete
    elif len([1 for t in CAL_DEL_WORDS if t in self.query]):

      # get name
      try:
        name = None
        name = [w for w in self.query if type(w) == dict and w["type"] == "event"]
        if len(name):
          name = name[0]


        # delete it
        for e in self.app.calender.events:
          if e["name"].strip() == name["name"].strip():
            self.app.calender.events.remove(e)
            self.app.calender.sync()
            self.resp["text"] = "Deleted %s" % name["name"]
            self.resp["status"] = STATUS_OK
            return

      except IndexError, KeyError:
        if name and type(name) == dict:
          self.resp["text"] = "Cannot find event named %s" % name["name"]
          self.resp["status"] = STATUS_OK
          return
