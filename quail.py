#!/usr/bin/python
import sys

def main():
  flask_args = {}

  # get args
  if len(sys.argv) > 1:
    if sys.argv[1] == "debug" or sys.argv[1] == "develop" or sys.argv[1] == "devel":
      flask_args["debug"] = True

  # append to path
  sys.path.append("src")

  # run App
  import app
  app.App(**flask_args)

if __name__ == '__main__':
  main()