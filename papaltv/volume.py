
class BaseVolume(object):
    """Interface to allow users to provide a list of items at a given location"""
    def __init__(self):
        super(BaseVolume, self).__init__()

    """should return True if the path is a valid directory, false otherwise"""
    def isdir(self,path):
        raise NotImplementedError("subclasses must override this")

    def is_list_view_dir(self,path):
        return False

    """should return a list of file names within the directory at the given path"""
    def listdir(self,path):
        raise NotImplementedError("subclasses must override this")

    """should return True if the path is a valid file, false otherwise"""
    def isfile(self,path):
        raise NotImplementedError("subclasses must override this")
