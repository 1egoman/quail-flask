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

def create_query_object(query, app):
  # create response object
  response = query.split(' ')
  response = format_day(response, query)
  response = format_time(response, query)
  response = format_events(response, query, app)
  response = format_people(response, query, app)
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

def format_time(response, query):

  # for ct,r in enumerate(response):
  #   if type(r) == str or type(r) == unicode:
  #     timeone = re.findall("([01]?[0-9]):([0-5][0-9]) ?(am|AM|pm|PM)", r)
  #     if len(timeone):
  #       now = dt.datetime.now()
  #       when = dt.datetime(year=now.year, month=now.month, day=now.day, hour=12+int(timeone[0][0]), minute=int(timeone[0][1]) )
  #       response = replace_inside_string(query, response, r, {"type": "time", "when": when.strftime("%c") })  

  return response


def format_day(response, query):

  # times
  now = dt.datetime.now()
  now = dt.datetime(year=now.year, month=now.month, day=now.day, hour=0, minute=0, second=0)
  delta = dt.timedelta()
  querytimedelta = dt.timedelta()
  timect = -1

  day_dict = {
    "monday": 1,
    "tuesday": 2,
    "wednesday": 3,
    "thursday": 4,
    "friday": 5,
    "saturday": 6,
    "sunday": 0
  }

  # check for times, merge any times with the dates
  for c, g in enumerate(response):
    
      try:
        if type(g) == str or type(g) == unicode:
          times = re.findall("([01]?[0-9]):([0-5][0-9]) ?(am|AM|pm|PM)", g)
          if len(times):
            querytimedelta = dt.timedelta(hours=12+int(times[0][0]), minutes=int(times[0][1]))
            response.remove(g)
            timect = c
            break
      except IndexError: pass


  # iterate through days
  for d,v in day_dict.items():

    # next day (next tuesday)
    if "next %s"%d in query:
      days_delta = v - (now.weekday()+1) + 7 # our day of week we are trying to go to
      delta += dt.timedelta(days=days_delta)
      response = replace_inside_string(query, response, "next")
      response = replace_inside_string(query, response, "tuesday", {"type": "time", "when": (now + delta + querytimedelta).strftime('%c')})
      return response

    # previous day (last tuesday)
    elif "last %s"%d in query:
      days_delta = v - (now.weekday()+1) - 7 # our day of week we are trying to go to
      delta += dt.timedelta(days=days_delta)
      response = replace_inside_string(query, response, "last")
      response = replace_inside_string(query, response, "tuesday", {"type": "time", "when": (now + delta + querytimedelta).strftime('%c')})
      return response

    # day of week (ex. tuesday)
    elif d in query:

      days_delta = v - (now.weekday()+1) # our day of week we are trying to go to
      if days_delta < 0: days_delta += 7 # always look to the future
      delta += dt.timedelta(days=days_delta)
      response = replace_inside_string(query, response, d, {"type": "time", "when": (now + delta + querytimedelta).strftime('%c')})
      return response

    elif "tommorow" in query:
      delta += dt.timedelta(days=1)
      response = replace_inside_string(query, response, "tommorow", {"type": "time", "when": (now + delta + querytimedelta).strftime('%c')})
      return response

    elif "yesterday" in query:
      delta += dt.timedelta(days=-1)
      response = replace_inside_string(query, response, "yesterday", {"type": "time", "when": (now + delta + querytimedelta).strftime('%c')})
      return response




  # day and the exact day (21st, or 2nd)
  specific_day = re.search(  "([0-9]?[0-9])(st|nd|rd|th)", query  )
  if specific_day and specific_day.group(1).isdigit():

    # find out days
    days_delta = int(specific_day.group(1))
    
    # always move foreward to the next month
    if days_delta <= now.day:
      month_delta = 1
    else:
      month_delta = 0

    # set it
    now = dt.datetime(day=days_delta, month=now.month, year=now.year)
    response = replace_inside_string(query, response, "%s%s" % (specific_day.group(1), specific_day.group(2)), {"type": "time", "when": format_time(now + delta + querytimedelta)})  
    return response    


  # otherwise...
  response[timect-1] = {"type": "time", "when": (now + querytimedelta).strftime('%c')}

  return response



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