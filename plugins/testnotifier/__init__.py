from plugin import *
from network import STATUS_OK
import datetime

class TestNotificationPlugin(Plugin):

  def __init__(self, *args, **kwargs):
    super(TestNotificationPlugin, self).__init__(*args, **kwargs)
    self.notifyUser = False

  def validate(self):
    return "notify" in self.query

  def parse(self):

    self.resp["status"] = STATUS_OK
    self.resp["text"] = "notifying..."
    self.notifyUser = True

  def listener(self):

    if self.notifyUser:
      self.notifyUser = False

      packet = Packet()
      packet["status"] = STATUS_OK
      packet["text"] = "Test notification!"
      self.app.stack.append(packet)