from plugin import Plugin
from network import STATUS_OK, STATUS_ERR
from datetime import datetime

class ExersizePlugin(Plugin):

  def validate(self):
    # print self.query.as_str()
    return "walk" in self.query.as_str() or "strength" in self.query.as_str() or (("push" in self.query.as_str() or "sit" in self.query.as_str()) and "up" in self.query.as_str())

  def parse(self):

    # make sure we already have not logged it
    now = datetime.now()
    today = self.app.calender.events.year( now.strftime('%Y') ).month( now.strftime('%b') ).day( now.strftime('%d') )
    if len(today) and len([ 1 for d in today if d.has_key("tags") and "exercise" in d["tags"] ]):
      self.resp["status"] = STATUS_OK
      self.resp["text"] = "You already did exercise today."
      return

    # what event?
    if "walk" in self.query.as_str():
      self.app.calender.add_event(name="Walking", when=datetime.now(), tags=["walk", "exercise", "nonotify"], color=self.info["color"])
      self.resp["status"] = STATUS_OK
      self.resp["text"] = "You are walking today."

    elif "strength" in self.query.as_str() or "weights" in self.query.as_str():
      self.app.calender.add_event(name="Strength", when=datetime.now(), tags=["strength", "exercise", "nonotify"], color=self.info["color"])
      self.resp["status"] = STATUS_OK
      self.resp["text"] = "You are doing strength today."

    elif "push" in self.query.as_str():
      digits = [int(s) for s in self.query.as_str().split() if s.isdigit()]
      if len(digits):
        d = digits[0]

        self.app.calender.add_event(name="%s Pushups" % d, when=datetime.now(), tags=["pushup", "exercise", "nonotify"], color=self.info["color"])
        self.resp["status"] = STATUS_OK
        self.resp["text"] = "Pushups noted"

    else:
      self.resp["status"] = STATUS_ERR