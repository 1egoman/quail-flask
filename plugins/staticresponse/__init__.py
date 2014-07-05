from plugin import *
from network import STATUS_OK
import json

class StaticResponsePlugin(Plugin):

  def __init__(self, *args, **kwargs):
    super(StaticResponsePlugin, self).__init__(*args, **kwargs)

  def validate(self): 
    # read phrases
    with open(  os.path.join(self.get_plugin_dir(__file__), "phrases.json")  ) as f:
      self.phrases = json.loads( f.read() )

    # validate
    querystr = ' '.join([str(a) for a in self.query])
    return len([1 for k,v in self.phrases.items() if k in querystr])

  def parse(self):
    # get phrase
    querystr = ' '.join([str(a) for a in self.query])
    phrase = [i for i in self.phrases if i in querystr]
    if len(phrase):
      longestphrase = sorted(phrase, key=lambda x: len(x))[-1]
      self.resp["text"] = self.phrases[ longestphrase ]
      self.resp["status"] = STATUS_OK
    else:
      self.resp["text"] = "phrase doesn't exist"
      self.resp["status"] = STATUS_NO_HIT


  def listener(self): pass 
    # packet = Packet()
    # packet["status"] = STATUS_OK
    # self.app.stack.append(packet)