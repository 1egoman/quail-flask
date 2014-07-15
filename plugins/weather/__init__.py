from plugin import *
from network import STATUS_OK
from json import loads, dumps
import weather as wtr
import datetime as dt

# day list
days = {
  "monday": 0,
  "tuesday": 1,
  "wednesday": 2,
  "thursday": 3,
  "friday": 4,
  "saturday": 5,
  "sunday": 6
}

# weather terms
weather_terms = ["weather", "rain", "sun", "cloud", "snow", "wind", "tempurature", "conditions", "storm", "advisory"]


class WeatherPlugin(Plugin):

  def __init__(self, *args, **kwargs):
    super(WeatherPlugin, self).__init__(*args, **kwargs)


  def validate(self):
    return len([1 for d in weather_terms if d in self.query])

  def parse(self):

    # get api key
    if self.info.has_key("key"):
      WEATHER_API_KEY = self.info["key"]
    else:
      self.resp["text"] = "bad key"
      self.resp["type"] = "weather"
      self.resp["status"] = STATUS_ERR
      return self.resp

    # define vars
    where = None
    times = ["am", "pm", "minutes", "tommorow", "yesterday"]
    times.extend(days)



    # if weather terms... get the weather
    if len([1 for d in weather_terms if d in self.query]):

      # determine when
      when = [w for w in self.query if type(w) == dict and w.has_key("type") and w["type"] == "time"]
      if len(when):
        out = dt.datetime.strptime(when[0]["when"], '%c').strftime("%Y:%m:%d:%X").replace("/", ":")
        when = [int(d) for d in out.split(":")]
      else:
        out = dt.datetime.now().strftime("%Y:%m:%d:%X").replace("/", ":")
        when = [int(d) for d in out.split(":")]


      wtr.parse_weather(self, when, "", WEATHER_API_KEY)

    # return
    self.resp["status"] = STATUS_OK


  def update_list(self):
    with open(os.path.join(self.get_plugin_dir(__file__), LIST_FILE), 'w') as j:
      j.write(dumps(self.lists, indent=2))


