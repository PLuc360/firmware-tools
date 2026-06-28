import os

def ListFolders(input_dir=[], extension_filter=[], recursive=False):
    """ Function to list folders containing files that have a given extension

    Arguments:
    - input_dir         [array]     input directory
    - extension_filter  [array]     Keeps only folders containing files with one of these extensions
    - recursive         [bool]      check recursively
    """
    result = []
    success = False

    for dir in input_dir:
        for file in os.listdir(dir):
            if os.path.isfile(os.path.abspath(dir) + '\\' + file):
                name, ext = os.path.splitext(file)
                if ext in extension_filter:
                    success = True
                    if dir not in result:
                        result.append(dir)
            elif recursive:
                paths=[]
                paths.append(os.path.abspath(dir) + '\\' + file)
                subsuccess, subresult = ListFolders(paths, extension_filter, recursive=recursive)
                if subsuccess:
                    success |= subsuccess
                    for subsubresult in subresult:
                        if subsubresult not in result:
                            result.append(subsubresult)

    return success, result