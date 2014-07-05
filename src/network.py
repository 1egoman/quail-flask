
# network status constants
STATUS_OK = "OK"
STATUS_ERR = "ERROR"
STATUS_NO_HIT = "NO_HIT"
STATUS_UNKNOWN = "UNKNOWN"

class Packet(dict):
  """
  Packets are used to transfer data from one server to another through json.
  p = Packet()
  p[key] = value
  """

  def __init__(self, *args, **kwargs):
    super(Packet, self).__init__(*args, **kwargs)

    # add files
    self.files = []

    # create required keys
    self["status"] = STATUS_UNKNOWN
    self["type"] = ""
    self["text"] = "No Response"


  def format(self):
    """ Format the packet as a dictionary """
    out = self.copy()
    out["files"] = self.files
    return out