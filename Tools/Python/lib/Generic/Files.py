import os

def ListFiles(input_dir, extension_filter=[], excluded_list=[], recursive=False):
    """ Function to list files from a given directory

    Arguments:
    - input_dir         [str]       input directory
    - extension_filter  [array]     only keep files with one of these extensions
    - excluded_list     [array]     file name exclusion list
    - recursive         [bool]      check recursively
    """
    result = []
    success = False

    for f in os.listdir(input_dir):
        fileName = os.path.join(input_dir, f)
        name, ext = os.path.splitext(fileName)
        if os.path.isfile(fileName) and (ext in extension_filter):
            success = True
            result.append(fileName)
        elif recursive and os.path.isdir(fileName) and (fileName not in excluded_list):
            subsuccess, subresult = ListFiles(fileName,
                                              extension_filter=extension_filter,
                                              excluded_list=excluded_list,
                                              recursive=recursive)
            if subsuccess:
                success = subsuccess
                result += subresult

    return success, result