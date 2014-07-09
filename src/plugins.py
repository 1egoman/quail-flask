import os, sys
from imp import load_source
from json import loads

class PluginManager(object):
  """
  This class does all the behind the scenes work of loading plugins.
  """

  def __init__(self, app, plugin_dir="plugins"):
    self.plugin_dir = os.path.abspath(plugin_dir)
    self.plugins = []
    self.app = app

  # load all plugins
  def load_all(self):

    # add 2 paths to be searched
    sys.path.append( os.path.abspath('.') )
    sys.path.append( self.plugin_dir )

    # look through possible plugin directorys
    for f in os.listdir(self.plugin_dir):
      if os.path.isfile(f): continue

      # see if the folder is a package
      try:
        plugin = {}
        plugin["package"] = __import__(f)

        # open config
        cfg = None
        cfg_path = os.path.abspath( os.path.join("plugins", f, "info.json") )
        with open( cfg_path ) as f:
          cfg = loads( f.read() )

        if cfg:
          # also, create the main plugin instance...
          exec "d = plugin[\"package\"].%s" % cfg["plugin"]
          plugin["instance"] = d(self)
          plugin["instance"].info = cfg

          # log what we did
          print " * loaded '%s': %s" % (cfg["name"], cfg["desc"])

          # add to plugins list
          self.plugins.append(plugin)

      except ImportError:
        pass


    # remove the paths
    sys.path.remove( os.path.abspath('.') )
    sys.path.remove( self.plugin_dir )