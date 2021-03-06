from flask import *#Flask, Response, url_for, jsonify, redirect, request, redner_template
from werkzeug.utils import secure_filename
from json import dumps, loads
import os
import datetime

from network import Packet, STATUS_OK, STATUS_NO_HIT, STATUS_ERR
from plugins import PluginManager
from calender import Calender
from files import UserFiles
from people import PeopleContainer
import wolfram
import listener

DEFAULTCONFIG = """{"host": "0.0.0.0", "port": 8000, "welcome": false}"""

class App(object):
  """ This class is the main app class, which starts Quail """
  flask = Flask(__name__)
  """ Contains the main flask instance """

  # quail version
  VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH = 1, 6, 'B'

  def __init__(self, **flask_args):

    cfgpath = os.path.join(self.get_root(), "config", "quail.json")

    # see if config exists
    if not os.path.exists(cfgpath):
      os.mkdir( os.path.dirname(cfgpath) )
      with open( cfgpath, 'w' ) as f:
        f.write(DEFAULTCONFIG)

    # read in config
    with open( cfgpath, 'r' ) as f:
      self.config = loads( f.read() )


    # add all api hooks
    self.add_api_hooks()

    # last plugin
    self.lastplugin = None

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

    self.run(**flask_args)


  def do_query(self, query="", plugin_name=None, n=0):
    """ Perform a query. Can be called by flask or another process """

    # get information about the user
    n = n or request.args.get("n") or 0
    self.user_type = request.args.get("type") or "human"

    # are we autorized?
    response = None

    if len(query):

      # check the last used plugin first
      if self.lastplugin: 
        response = self.run_plugin(self.lastplugin, query)

      # locate correct plugin
      if not response:
        for plugin in self.manager.plugins:
          response = self.run_plugin(plugin, query)
          if response: 
            break

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


    
    # return the response
    return Response(dumps(out),  mimetype='application/json')

  def run_plugin(self, plugin, query):
    """ Run a plugin if it can accept the query """
    # set new query, and validate
    plugin["instance"].new_query(query)
    if plugin["instance"].validate():

      # add to history, if human-made
      if "human" in self.user_type:
        self.lastplugin = plugin

      # parse the query
      plugin["instance"].parse()
      return plugin["instance"].resp
    return None

  def upload_resource(self, secret): 
    """ Upload a resource to quail so it can be parsed/used in a query """
    response = Packet()
    if request.method == 'POST':
      file = request.files['file']
      filename = secure_filename(file.filename)
      if fileg:
        file.save(os.path.join(self.config["upload-folder"], filename))

        response["status"] = STATUS_OK
        response["text"] = filename
        return Response(dumps( response.format() ),  mimetype='application/json')

  def web_gui(self, secret, plugin=None, path="/"):
    """ Web interface for quail interaction """
    html = ""
    root = ""

    # quail's site
    if not plugin:

      if request.args.has_key("query"):
        text = request.args.get("query")
        q = loads(self.do_query(self.config["secret"], query=text, n=1).data)
        html = render_template(  os.path.join(root, "old/query.html"), query=q  )

      elif path == "/":
        t = ""
        for plugin in self.manager.plugins:
          html = plugin["instance"].html_provider()
          if html:
            t += "<div class=\"plugin\"><div class=\"title\">%s</div><div class=\"data\">%s</div></div>" % (plugin["instance"].__class__.__name__, html)
        html = render_template( os.path.join(root, "old/index.html"), body=t)

    return html




  def calendar(self, month=0, year=0):
    """ Web interface for quail interaction """
    root = ""
    
    # format events to be displayed
    out = []
    now = datetime.datetime.today()


    # find year
    if year: 
      now = now.replace(year=int(year))


    # find months
    if month: 
      now = now.replace(month=int(month))



    # get previous month
    one_day = datetime.timedelta(days=1)
    last_month = now - one_day
    while last_month.month == now.month or last_month.day > now.day:
      last_month -= one_day

    try:
      days_in_month = (datetime.date(now.year, now.month+1, 1) - datetime.date(now.year, now.month, 1)).days
    except ValueError:
      days_in_month = 31 # must be december

    try:
      day_in_last_month = (datetime.date(last_month.year, last_month.month+1, 1) - datetime.date(last_month.year, last_month.month, 1)).days
    except ValueError:
      day_in_last_month = 31 # must be december



    # all days into a list
    for i in xrange(0, days_in_month+1):
      events_for_day = self.calender.events.year(now.year).month(now.month).day(i+1)

      today = {"day": i+1, "events": events_for_day, "month": "in"}
      out.append(today)
    


    # prepend previous month days
    for i in xrange( 0, int(datetime.date(now.year, now.month, 1).strftime('%w')) ):
      events_for_day = self.calender.events.year(now.year).month(now.month-1).day(i+1)

      today = {"day": day_in_last_month-i, "events": events_for_day, "month": "out"}
      out.insert(0, today)




    # split the output into weeks
    weeksout = []
    week_ct = -1;
    for i in xrange(0, days_in_month+i+1):
      if i%7 == 0:
        week_ct += 1
        weeksout.append([])
      try:
        weeksout[week_ct].append(out[i])
      except IndexError: pass


    # render output
    return render_template( os.path.join(root, "cal.html"), events=weeksout, title=now.strftime("%B %Y"),now=now)


  def web(self):
    """ Web interface for quail interaction """
    root = ""
    
    # first time?
    if not self.config.has_key("welcome") or (self.config.has_key("welcome") and not self.config["welcome"]):
      return render_template( os.path.join(root, "welcome.html"))
    else:
      return render_template( os.path.join(root, "index.html"))


  def updatequaildotjson(self):
    """ Update config/quail.json file """
    cfgpath = os.path.join(self.get_root(), "config", "quail.json")

    if request.args.get("data") and self.config["welcome"] == False:
      with open( cfgpath, 'w' ) as f:
        try:
          data = loads( request.args.get("data") )
          data["welcome"] = True
          self.config["welcome"] = True
          f.write( dumps(data) )
        except TypeError:
          f.write( dumps(self.config) )
          return "BAD"

      return "OK"
    return "NO DATA OR PERMISSION DENIED"


  def web_query(self):
    q = self.do_query( request.args.get('q') )
    return render_template( "query.html", query=loads(q.data) )
    
  def run(self, **flask_args):
    """ Sets all the flask options behind the scenes, and starte Flask """

    # multiple rules for a query
    self.flask.add_url_rule("/v2/<secret>/query", "query", view_func=self.do_query)
    self.flask.add_url_rule("/v2/<secret>/query/<query>", "query", view_func=self.do_query)
    self.flask.add_url_rule("/v2/<secret>/query/<query>/<int:n>", "query", view_func=self.do_query)
    self.flask.add_url_rule("/v2/<secret>/query/<query>/use/<plugin_name>", "query", view_func=self.do_query)
    self.flask.add_url_rule("/v2/<secret>/query/<query>/use/<plugin_name>/<int:n>", "query", view_func=self.do_query)

    # uploading of files
    self.flask.add_url_rule("/v2/<secret>/upload", "upload", methods=["POST"], view_func=self.upload_resource)

    # web interface
    self.flask.add_url_rule("/v2/<secret>/web", "web", view_func=self.web_gui)
    self.flask.add_url_rule("/v2/<secret>/web/<path>", "web", view_func=self.web_gui)
    self.flask.add_url_rule("/v2/<secret>/<plugin>/web", "web", view_func=self.web_gui)
    self.flask.add_url_rule("/v2/<secret>/<plugin>/web/<path>", "web", view_func=self.web_gui)

    # web interface
    self.flask.add_url_rule("/", "newweb", view_func=self.web)

    self.flask.add_url_rule("/cal", "web_cal", view_func=self.calendar)
    self.flask.add_url_rule("/cal/<int:month>", "web_cal", view_func=self.calendar)
    self.flask.add_url_rule("/cal/<int:month>/<int:year>", "web_cal", view_func=self.calendar)

    self.flask.add_url_rule("/search", "query_search", view_func=self.web_query)
    self.flask.add_url_rule("/quail.json", "updatequaildotjson", view_func=self.updatequaildotjson)

    # run flask
    self.flask.run(host=self.config["host"], port=self.config["port"], **flask_args)

  def get_root(self):
    """ Get root Quail directory """
    return os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )

  def add_api_hooks(self):
    """ Add api hooks for plugins to access later on, like people, events, etc """
    self.calender = Calender(self)
    self.files = UserFiles(self)
    self.people = PeopleContainer(self)