import os

def dir_path(string):
    """Function to check if the given path is a directory.

    Arguments:
    - string: [str]] path of the directory
    """
    # assert params
    assert isinstance(string, str)

    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

def file_path(string):
    """Function to check if the given path is a file.

    Arguments:
    - string: [str] path of the file
    """
    # assert params
    assert isinstance(string, str)

    if os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string)