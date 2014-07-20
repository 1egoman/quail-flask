import datetime as dt
import urllib2
import json



def parse_weather(self, when, where, API_KEY):


    conditions = None
    today = False
    # if there is no time, create one (means most likely that weather for today is requested)
    if not (type(when) == list and when[2] != dt.datetime.now().day):
      when = [dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day]

      # get today's conditions
      u = urllib2.urlopen("http://api.wunderground.com/api/%s/conditions/q/autoip.json" % API_KEY)
      todayconditions = json.loads( u.read() )["current_observation"]
      today = True

    # get from api
    u = urllib2.urlopen("http://api.wunderground.com/api/%s/forecast10day/q/autoip.json" % API_KEY)
    weather = json.loads( u.read() )
    weather = weather["forecast"]["simpleforecast"]["forecastday"]


    # find correct day
    w = [w for w in weather if w["date"]["year"] == when[0] and w["date"]["month"] == when[1] and w["date"]["day"] == when[2]]
    
    if len(w):

      # get weather
      weather = w[0]
      conditions = weather["conditions"].lower()
      temp = "a high of %s degrees, and a low of %s degrees" % (weather["high"]["fahrenheit"], weather["low"]["fahrenheit"])
      high, low = float(weather["high"]["fahrenheit"]), float(weather["low"]["fahrenheit"])
    else:

      # no conditions in query
      self.resp["text"] = "no weather available"
      return


    # tempurature
    if "tempurature" in self.query:
      if today:
        self.resp["text"] = "%s degrees" % todayconditions["feelslike_f"]
      else:
        self.resp["text"] = "high of %s degrees, and low of %s" % (high, low)
      return


    elif "high" in self.query:
      self.resp["text"] = "%s degrees" % high
      return


    elif "low" in self.query:
      self.resp["text"] = "%s degrees" % low
      return


    elif "conditions" in self.query:
      self.resp["text"] = conditions
      return


    elif "rain" in self.query or "storm" in self.query or "snow" in self.query:

      # get when it is happening
      if today:
        p = "it is %sing"
      else:
        p = "it will %s"

      if "rain" in conditions or "storm" in conditions or "snow" in conditions:
        self.resp["text"] = p % "rain"
        self.resp["color"] = "blue"
      else:
        self.resp["text"] = p % "not rain"
      return 


    elif "sun" in self.query:

      # get when it is happening
      if today:
        p = "it is %s"
      else:
        p = "it will be %s"

      if "sun" in conditions:
        self.resp["text"] = p % "sunny"
        self.resp["color"] = "yellow"
      else:
        self.resp["text"] = p % "not sunny"
      return 


    elif "cloud" in self.query:

      # get when it is happening
      if today:
        p = "it is %s"
      else:
        p = "it will be %s"

      if "cloud" in conditions:
        self.resp["text"] = p % "cloudy"
        self.resp["color"] = "blue"
      else:
        self.resp["text"] = p % "not cloudy"
      return 


    elif "weather" in self.query:
      if today:
        self.resp["text"] = "%s degrees, and %s" % (todayconditions["feelslike_f"], conditions)
      else:
        self.resp["text"] = "high of %s degrees, low of %s, and %s for %s %s, %s" % (high, low, conditions, dt.datetime.strptime(str(when[1]), '%m').strftime('%B'), when[2], when[0])
