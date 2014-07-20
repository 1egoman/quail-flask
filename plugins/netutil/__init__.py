from plugin import *
from network import STATUS_OK
import re

class NetUtilPlugin(Plugin):

  def validate(self):
    return "ip" in self.query

  def parse(self):

    if len( re.findall("(client|my)'?s? ip", self.query.as_str() ) ):
      self.resp["status"] = STATUS_OK
      self.resp["text"] = self.get_client_ip()

    if len( re.findall("(server|remote)'?s? ip", self.query.as_str() ) ):
      self.resp["status"] = STATUS_OK
      import socket
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      s.connect(('google.com', 0))
      self.resp["text"] = s.getsockname()[0]
      s.close()