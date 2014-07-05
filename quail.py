#!/usr/bin/python
import sys

def main():
  sys.path.append("src")
  import app
  app.App()

if __name__ == '__main__':
  main()