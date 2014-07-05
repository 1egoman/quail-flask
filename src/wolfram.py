from network import *
import xml.etree.ElementTree as et
import urllib2


def parse(query, API_KEY):
  """ Parse Wolfram Alpha for a result """
  resp = Packet()

  # set data type of packet
  resp["type"] = "wolfram"

  # query
  h = urllib2.urlopen("http://api.wolframalpha.com/v2/query?input="+query.replace(" ", "%20")+"&appid="+API_KEY)
  xml = h.read()
  root = et.fromstring(xml)

  # sub data type
  resp["subtype"] = root.attrib["datatypes"]

  # parse now
  for pod in root:
    if pod.tag == "pod":
      # loop through pod now
      # don't even check input pods
      if "Input" in pod.attrib["title"]: continue

      # check through sub pod's to find any plaintext
      for sp in pod:
        # look at tags inside subpod
        for t in sp:
          if t.tag == "plaintext":
            resp["text"] = t.text.replace("\n", " ").replace(" | ", ": ")

            if t.text and " | " in t.text:
              resp["return"] = [g.split(" | ") for g in t.text.split("\n") if g]
            elif t.text:
              resp["return"] = t.text.split("\n")
            else:
              resp["return"] = None

            # close socket
            h.close()

            # return response packet
            resp["status"] = STATUS_OK
            return resp
