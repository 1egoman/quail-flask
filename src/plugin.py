from flask import request
from network import Packet
import queryobject
import os

class Plugin(object):
  """
  Main class for a plugin.
  """

  def __init__(self, parent):
    self.parent = parent
    self.app = parent.app
    self.resp = Packet()


  def new_query(self, query=""):
    """
    Called before a query. Resets query and the packet.
    """

    # set query
    self.query = queryobject.create_query_object( query )

    # set response
    self.resp = Packet()
    self.resp["type"] = self.__class__.__name__


  def get_plugin_dir(self, f): # f should be __file__
    """ gets the directory of the plugin. f should equal __file__ """
    d = f.split(os.sep)[-2]
    return os.path.abspath( os.path.join("plugins", d) )

  def get_client_ip(self):
   return request.remote_addr



  def validate(self): return False
  def parse(self): pass