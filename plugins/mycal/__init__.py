from plugin import Plugin
from network import STATUS_OK, Packet
import datetime as dt
import time
import re

CAL_ADD_WORDS = ["named", "called", "create", "add"]
CAL_DEL_WORDS = ["named", "called", "check", "delete", "remove"]
STRIP_WORDS = ["to", "from", "on", "in", "by", "list"]
WHEN_WORDS = ["at", "for"]

notified = []

class CalPlugin(Plugin):

  def validate(self):
    return "calender" in self.query or "calendar" in self.query or "event" in self.query.as_str() or len(re.findall("(happening|going on)", self.query.as_str()))

  def listener(self):
    now = dt.datetime.now()

    # any events coming up?
    for event in self.app.calender.events:
      try:
        when = dt.datetime.strptime(event["when"], '%c')
      except TypeError:
        when = dt.datetime.strptime(event["when"][0], '%c')

      donotify = (event.has_key("tags") and "nonotify" not in event["tags"]) or (not event.has_key("tags"))
      if when.hour == now.hour and when.minute == now.minute and donotify and event["name"] not in notified:
        # notify
        notified.append(event["name"])
        # print when, "NOTIFY!!!!"

        pkt = Packet()
        pkt["status"] = STATUS_OK
        pkt["text"] = "Calender: %s" % event["name"]
        self.app.stack.append(pkt)

  def parse(self):

    # add
    if len([1 for t in CAL_ADD_WORDS if t in self.query]):

      # get when
      timeq = None
      when = [w for w in self.query if type(w) == dict and w["type"] == "time"]
      if len(when):
        timeq = dt.datetime.strptime(when[0]["when"], '%c')
      
      # get name
      start = None
      name = ""
      for ct,r in enumerate(self.query):

        if r in CAL_ADD_WORDS:
          start = ct+1

        elif start != None and r in STRIP_WORDS:
            if len([1 for d in self.query[start:ct] if type(d) == dict and d["type"] == "event"]):
              self.resp["text"] = "Event already exists!"
              self.resp["status"] = STATUS_OK
              return
            else:
              name = ' '.join(   self.query.as_str().split(' ')[start:ct]   )
              break

      # add it
      self.app.calender.add_event(name=name, when=timeq)

      self.resp["status"] = STATUS_OK
      self.resp["text"] = "Added %s to %s" % ( name, timeq.strftime("%A, %B %d, %Y") )

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

    else:

      # just list
      when = [a for a in self.query if type(a) == dict and a["type"] == "time"]

      if len(when):
        # day is when
        when = dt.datetime.strptime(when[0], '%c')
      else:
        # day is today
        when = dt.datetime.today()

      events = self.app.calender.events.year(when.year).month(when.month).day(when.day)
      foundevents = events and re.findall(  "(%s)" % '|'.join([a["name"] for a in events]), self.query.as_str()  )

      # are these events in the query?
      if foundevents and len(foundevents):
        self.resp["text"] = ','.join( foundevents )
      else:
        # just list all
        self.resp["text"] = ' '.join(events) or "Nothing Today"
        self.resp["status"] = STATUS_OK





  def html_provider(self, maxevents=8):
    d = "Today:<ul>"
    for e in self.app.calender.events.day(dt.datetime.now().day)[:maxevents]:
      d += "<li style='list-style-type: none;'><span style=\"font-weight: bold;'\">%s</span> on %s " % ( e["name"], dt.datetime.strptime(e["when"], '%c').strftime("%A, %B %d at %I:%M %p") )
    return d