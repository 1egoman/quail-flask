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


def create_query_object(query):

  # create response object
  response = query.split(' ')

  # times
  now = dt.datetime.now()
  delta = dt.timedelta()

  day_dict = {
    "monday": 1,
    "tuesday": 2,
    "wednesday": 3,
    "thursday": 4,
    "friday": 5,
    "saturday": 6,
    "sunday": 0
  }

  # iterate through days
  for d,v in day_dict.items():

    # next day (next tuesday)
    if "next %s"%d in query:
      days_delta = v - (now.weekday()+1) + 7 # our day of week we are trying to go to
      delta += dt.timedelta(days=days_delta)
      response = replace_inside_string(query, response, "next")
      response = replace_inside_string(query, response, "tuesday", {"type": "time", "when": format_time(now + delta)})

    # previous day (last tuesday)
    elif "last %s"%d in query:
      days_delta = v - (now.weekday()+1) - 7 # our day of week we are trying to go to
      delta += dt.timedelta(days=days_delta)
      response = replace_inside_string(query, response, "last")
      response = replace_inside_string(query, response, "tuesday", {"type": "time", "when": format_time(now + delta)})

    # day of week (ex. tuesday)
    elif d in query:

      days_delta = v - (now.weekday()+1) # our day of week we are trying to go to
      if days_delta < 0: days_delta += 7 # always look to the future
      delta += dt.timedelta(days=days_delta)
      response = replace_inside_string(query, response, d, {"type": "time", "when": format_time(now + delta)})

    elif "tommorow" in query:
      delta += dt.timedelta(days=1)
      response = replace_inside_string(query, response, "tommorow", {"type": "time", "when": format_time(now + delta)})

    elif "yesterday" in query:
      delta += dt.timedelta(days=-1)
      response = replace_inside_string(query, response, "yesterday", {"type": "time", "when": format_time(now + delta)})




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
    response = replace_inside_string(query, response, "%s%s" % (specific_day.group(1), specific_day.group(2)), {"type": "time", "when": format_time(now + delta)})       

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

# turn time into list of [year, month, day, hour, minute, sec]
def format_time(t):
  out = t.strftime("%Y:%m:%d:%X").replace("/", ":")
  return [int(d) for d in out.split(":")]

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

if __name__ == '__main__':
  print create_query_object("tuesday the 2nd")