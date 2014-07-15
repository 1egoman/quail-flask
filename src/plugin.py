from flask import request
from network import Packet
import queryobject
import os

# try and import nltk
try:
  import nltk
except ImportError:
  nltk = None


class Plugin(object):
  """
  Main class for a plugin.
  """

  def __init__(self, parent):
    self.parent = parent
    self.app = parent.app
    self.resp = Packet()
    self.query = None
    self.history = []


  def new_query(self, query=""):
    """
    Called before a query. Resets query and the packet.
    """

    # set query
    if self.query: self.history.append( self.query )
    self.query = Query( queryobject.create_query_object( query, app=self.app) )

    # set response
    self.resp = Packet()
    self.resp["type"] = self.__class__.__name__


  def get_plugin_dir(self, f): # f should be __file__
    """ gets the directory of the plugin. f should equal __file__ """
    d = f.split(os.sep)[-2]
    return os.path.abspath( os.path.join("plugins", d) )

  def get_client_ip(self):
    """ Returns the client's IP address """
    return request.remote_addr

  def did_previous_query(self):
    """ Did this plugin do the previous query? """
    return bool( self.app.lastplugin and self.app.lastplugin["instance"] == self )

  def get_me(self):
    """ Gtet info about the person being talked to """
    out = [a for a in self.app.people.data if type(a) == dict and a.has_key("tags") and "me" in a["tags"]]
    if len(out):
      return out
    else:
      return None

  def html_provider(self):
    return ""


  def validate(self): return False
  def parse(self): pass


class Query(list):
  """ List-based object that represents each query made """

  def as_str(self):
    """ Return the query parsed as a string """
    out = []
    for i in self:
      if type(i) == dict:
        out.append( i["text"] )
      else:
        out.append( str(i) )
    return ' '.join(out)

  def as_nltk(self):
    """ Return the query parsed with nltk, will return None if nltk cannot be imported """
    if nltk:
      tokens = nltk.word_tokenize( self.as_str() )
      tagged = nltk.pos_tag(tokens)
      return tagged
    else:
      return None

  def as_all(self):
    """ Mixes as_nltk and the normal list attributes """
    nltk_parsed = self.as_nltk()
    query = self[:]

    for ct,item in enumerate(query):
      if type(item) == str or type(item) == unicode:
        query[ct] = nltk_parsed[ct]

    return query