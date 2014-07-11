import json
import datetime as dt
import re


# month list
months = {
  1: "january", 
  2: "febuary", 
  3: "march", 
  4: "april", 
  5: "may", 
  6: "june", 
  7: "july", 
  8: "augest", 
  9: "september", 
  10: "october", 
  11: "november", 
  12: "december"
}

days_dict = {
  "monday": 0,
  "tuesday": 1,
  "wednesday": 2,
  "thursday": 3,
  "friday": 4,
  "saturday": 5,
  "sunday": 6
}

def create_query_object(query, app):
  # create response object
  response = query.replace('+', ' ').split(' ')
  response = format_time(response, query)
  response = format_events(response, query, app)
  response = format_people(response, query, app)
  print response
  return response


def format_events(response, query, app):

  # go through each word
  for evt in app.calender.events:
    if (type(evt["name"]) == str or type(evt["name"]) == unicode) and evt["name"] in query:
      cp = evt.copy()
      cp["type"] = "event"
      response = replace_inside_string( query, response, evt["name"], cp )

  return response

def format_people(response, query, app):
  # Does the query have at least 2 relevent bits of information pertaining to a person? If so, return the person's info
  people = app.people.data
  SUFFIXES = ["", "'s", "ies"]

  for p in people:
    keyin = 0
    for k, v in p.items():
      papp = p.copy()
      papp["type"] = "person"

      # if the values are in the query
      if type(v) == list:
        for w in v:
          for s in SUFFIXES:
            if "%s%s" % (w, s) in response: 
              response = replace_inside_string( query, response, "%s%s" % (w, s), papp )
      else:
        if v in response or "%s's" % v in response:
          response = replace_inside_string( query, response, v, papp )
          response = replace_inside_string( query, response, "%s's" % v, papp )

  return response

def format_time(resp, query):


  # do the real detection
  c_times = re.compile("([0-2]?[0-9]):([0-6]?[0-9]) ?(pm|PM|Pm|p\.m\.|am|AM|Am|a\.m\.)?")
  c_times_oclock = re.compile("([0-2]?[0-9]) ?o'?.?clock.? ?(pm|PM|Pm|p\.m\.|am|AM|Am|a\.m\.)?")
  c_days = re.compile("(Monday|monday|Mon|mon|Tuesday|tuesday|tue|Tue|Wednesday|wednesday|Wed|wed|Thursday|thursday|thurs|Thurs|Friday|friday|Fri|fri|Saturday|saturday|sat|Sat|Sunday|sunday|sun|Sun)")
  c_days_and_times = re.compile("(Mon|mon|Monday|monday|Tue|Tuesday|tuesday|tue|Wed|wed|Wednesday|wednesday|thurs|Thurs|Thursday|thursday|Fri|fri|Friday|friday|sat|Sat|Saturday|saturday|sun|Sun|Sunday|sunday) .* ?([0-2]?[0-9]):([0-6]?[0-9]) ?(pm|PM|Pm|p\.m\.|am|AM|Am|a\.m\.)")
  
  # if both matched...
  if len(tuple(c_days_and_times.finditer(query))):

  # get any dates and times in phrase
  # EX: Tuesday at 5:30 pm
    for match in c_days_and_times.finditer(query):

      # get all words following time
      wordsupto = query[:match.start()]

      # get where to start replacement, and how many words to replace
      startreplaceat = len(wordsupto.strip().split(' '))
      endreplaceat = startreplaceat + len(match.group().split(' '))

      # convert the user's time to a datetime object
      timestr = "%s:%s %s" % (  match.group(2), match.group(3), match.group(4).upper().replace('.', '')  )
      dtobj = dt.datetime.strptime(timestr, "%I:%M %p")

      # same as above but for the days
      today = dt.datetime.today()
      days = [v for k,v in days_dict.items() if match.group(1).lower() in k]
      if len(days):
        # calculate days until the requested day
        days_until = (days[0] - today.weekday() + 7) % 7
      else:
        days_until = 0 # ??? why would this ever land here?

      # create the datetime object
      time = dt.datetime.combine(   dt.datetime.now() + dt.timedelta(days=days_until), dt.time(dtobj.hour, dtobj.minute, dtobj.second)   )

      # create the data structure
      data = {"type": "time", "when": time.strftime('%c'), "text": match.group(0)}

      # do the replacing
      resp[startreplaceat] = data
      resp[startreplaceat+1:endreplaceat] = ''


  # if just the time matched...
  elif len(tuple(c_times.finditer(query))):

    # get any times in phrase
    # EX: 5:30 pm
    for match in c_times.finditer(query):

      # get all words following time
      wordsupto = query[:match.start()]

      # get where to start replacement, and how many words to replace
      startreplaceat = len(wordsupto.strip().split(' '))
      endreplaceat = startreplaceat + len(match.group().split(' '))

      # convert the user's time to a datetime object
      if match.group(3):
        timestr = "%s:%s %s" % (  match.group(1), match.group(2), match.group(3).upper().replace('.', '')  )
      else:
        timestr = "%s:%s %s" % (  match.group(1), match.group(2), dt.datetime.now().strftime("%p")  )
      dtobj = dt.datetime.strptime(timestr, "%I:%M %p")
      time = dt.datetime.combine(   dt.datetime.now(), dt.time(dtobj.hour, dtobj.minute, dtobj.second)   )

      # create the data structure
      data = {"type": "time", "when": time.strftime('%c'), "text": match.group(0)}

      # do the replacing
      resp[startreplaceat] = data
      resp[startreplaceat+1:endreplaceat] = ''


  # if just the time matched (the oclock version)
  elif len(tuple(c_times_oclock.finditer(query))):

    # get any times in phrase
    # EX: 5:30 pm
    for match in c_times_oclock.finditer(query):

      # get all words following time
      wordsupto = query[:match.start()]

      # get where to start replacement, and how many words to replace
      startreplaceat = len(wordsupto.strip().split(' '))
      endreplaceat = startreplaceat + len(match.group().split(' '))

      # convert the user's time to a datetime object
      if match.group(2):
        timestr = "%s:00 %s" % (  match.group(1), match.group(2).upper().replace('.', '')  )
      else:
        timestr = "%s:00 %s" % (  match.group(1), dt.datetime.now().strftime("%p")  )
      dtobj = dt.datetime.strptime(timestr, "%I:%M %p")
      time = dt.datetime.combine(   dt.datetime.now(), dt.time(dtobj.hour, dtobj.minute, dtobj.second)   )

      # create the data structure
      data = {"type": "time", "when": time.strftime('%c'), "text": match.group(0)}

      # do the replacing
      resp[startreplaceat] = data
      resp[startreplaceat+1:endreplaceat] = ''


  # if just the days matched...
  elif len(tuple(c_days.finditer(query))):

    # get any day only in phrase
    # EX: Tuesday
    for match in c_days.finditer(query):

      # get all words following time
      wordsupto = query[:match.start()]

      # get where to start replacement, and how many words to replace
      startreplaceat = len(wordsupto.strip().split(' '))
      endreplaceat = startreplaceat + len(match.group().split(' '))

      # convert the user's time to a datetime object
      today = dt.datetime.today()
      days = [v for k,v in days_dict.items() if match.group(1).lower() in k]
      if len(days):
        # calculate days until the requested day
        days_until = (days[0] - today.weekday() + 7) % 7
      else:
        days_until = 0 # ??? why would this ever land here?

      # calculate datetime object
      time = dt.datetime.now() + dt.timedelta(days=days_until)

      # create the data structure
      data = {"type": "time", "when": time.strftime('%c'), "text": match.group(0)}

      # do the replacing
      resp[startreplaceat] = data
      resp[startreplaceat+1:endreplaceat] = ''

  return resp



# get end pos of 'words' words starting at pos
def get_words(string, pos, words=1):
  wordct = 0 # amount of words
  for c,w in enumerate(  string[pos:].strip()  ):
    # new word
    if w == ' ': wordct += 1

    # at limit?
    if wordct >= words:
      return pos+c


# replace the specified word(s) with an object
def replace_inside_string(query, resp, word, what=None):
  if what and word in resp:
    inx = resp.index(word)
    resp[ inx ] = what
    if type(what) == dict:
      resp[ inx ]["text"] = word
  elif word in resp:
    resp.remove(word)


  # return
  return resp