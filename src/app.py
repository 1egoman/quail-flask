from flask import Flask, Response, url_for, jsonify
from json import dumps, loads
import os

from network import Packet, STATUS_OK, STATUS_NO_HIT, STATUS_ERR
from plugins import PluginManager
from calender import Calender
import wolfram
import listener

DEFAULTCONFIG = """"""

class App(object):
  """ This class is the main app class, which starts Quail """
  flask = Flask(__name__)

  def __init__(self):

    cfgpath = os.path.join(self.get_root(), "config", "quail.json")

    # see if config exists
    if not os.path.exists(cfgpath):
      with open( cfgpath, 'w' ) as f:
        f.write(DEFAULTCONFIG)

    # read in config
    with open( cfgpath, 'r' ) as f:
      self.config = loads( f.read() )


    # add all api hooks
    self.add_api_hooks()

    # create plugin manager
    self.manager = PluginManager(self)
    self.manager.load_all()

    # create stack
    self.stack = []

    # start listener thread
    thrd = listener.listenerThread(self, self.manager.plugins)
    thrd.setName("threadListener")
    thrd.daemon = True
    thrd.start()

    self.run()


  def do_query(self, secret, query="", plugin_name=None, n=0):
    """ Perform a query. Can be called by flask or another process """

    # are we autorized?
    if secret == self.config["secret"]:
      response = None

      if len(query):

        # locate correct plugin
        for plugin in self.manager.plugins:

          # set new query, and validate
          plugin["instance"].new_query(query)
          if plugin["instance"].validate():

            # found the right plugin!
            # parse the query
            plugin["instance"].parse()
            response = plugin["instance"].resp

        # if there is no response, try and parse something from wolfram alpha
        if not response: response = wolfram.parse(query, self.config["wa-api-key"])

        # still no response: error
        if not response:
          response = Packet()
          response["status"] = STATUS_NO_HIT


        # add the response to the stack
        out = response.format()
        self.stack.append(out)
      
      # n is the amount of packets to return
      if n == 0:
        # return all of them
        out = self.stack
        self.stack = []
      else:
        # return 'n' packets
        out = self.stack[-n:]
        self.stack = self.stack[:-n]

    else:
      response = Packet()
      response["status"] = STATUS_ERR
      response["text"] = "incorrect secret"
      out = response.format()

    
    # return the response
    return dumps(out)
    
  def run(self):

    # multiple rules for a query
    self.flask.add_url_rule("/v2/<secret>/query", "query", view_func=self.do_query)
    self.flask.add_url_rule("/v2/<secret>/query/<query>", "query", view_func=self.do_query)
    self.flask.add_url_rule("/v2/<secret>/query/<query>/<int:n>", "query", view_func=self.do_query)
    self.flask.add_url_rule("/v2/<secret>/query/<query>/use/<plugin_name>", "query", view_func=self.do_query)
    self.flask.add_url_rule("/v2/<secret>/query/<query>/use/<plugin_name>/<int:n>", "query", view_func=self.do_query)

    # run flask
    self.flask.run(host=self.config["host"], port=self.config["port"])

  def get_root(self):
    return os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )

  def add_api_hooks(self):
    self.calender = Calender(self)