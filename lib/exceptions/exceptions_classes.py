"""
Exceptions linked to folders names errors
"""


class PathNotFoundError(Exception):
    """
    Tells that the path was not found
    """
    def __init__(self, path_name):
        self.pathname = path_name

    def __repr__(self):
        return 'Impossible to find the path {}.'.format(self.pathname)

class AlreadyExistsError(Exception):
    """
    Tells that the file already exists
    """
    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return "The file {} already exists.".format(self.path)

class NoDataToAddError(Exception):
    """
    Tells that we cannot add data to file """
    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return "There is no data to add to the file {}".format(self.path)