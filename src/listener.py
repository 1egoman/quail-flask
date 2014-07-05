from threading import Thread
import time

class listenerThread(Thread):
  """ Thread that runs all the listeners each frame """

  def __init__(self, parent, pl):
    Thread.__init__(self)
    self.plugins = pl
    self.parent = parent

  def run(self):
    while 1:
      # loop through all plugins
      for p in self.plugins:

        # only worry about plugins with listeners
        if not hasattr(p["instance"], "listener"): continue

        # run it
        p["instance"].listener()

      # delay before next frame
      time.sleep(1)