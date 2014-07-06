from plugin import *
from network import STATUS_OK
from json import loads, dumps
import wolfram
from datetime import datetime

class DateTimePlugin(Plugin):
  """ Parses wolfram alpha's time output better for tts programs """

  def __init__(self, *args, **kwargs):
    super(DateTimePlugin, self).__init__(*args, **kwargs)


  def validate(self): 
    return "time" in self.query or "date" in self.query

  def parse(self): 

    self.resp["status"] = STATUS_OK

    # first, start with what wolfram alpha has to say
    querystring = ' '.join([str(q) for q in self.query])
    w_out = wolfram.parse(querystring[:].replace("date", "time"), self.app.config["wa-api-key"])["text"]

    # do some parsing
    if "time" in querystring:
      ourtime = ''.join(w_out.split(" : ")[0].split(' ')[:-1])
      ourtime = datetime.strptime(ourtime, "%I:%M:%S%p")
      self.resp["text"] = ourtime.strftime("%I:%M %p")

    elif "date" in querystring:
      ourdate = ''.join(w_out.split(" : ")[-1])
      self.resp["text"] = ourdate.strip()

    else:
      self.resp["status"] = STATUS_NO_HIT