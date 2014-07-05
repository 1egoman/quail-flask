import os

class UserFiles(object):
  """ Contains all files uploaded by a user """

  def __init__(self, app):
    self.app = app
    self.upload_dir = os.path.abspath( self.app.config["upload-folder"] )

    # make sure folder exists
    if not os.path.isdir(self.upload_dir):
      os.mkdir(self.upload_dir)

  def get(self, name, mode='r'):
    """ get file object of a file in the uploads folder """
    path = os.path.join(self.upload_dir, name)
    return open(path, mode)