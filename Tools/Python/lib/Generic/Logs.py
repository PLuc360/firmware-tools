import os
import sys

# Class of different styles
class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

LOG_COLOR = {
    "DEBUG"  : style.BLUE,
    "INFO"   : style.GREEN,
    "WARNING": style.YELLOW,
    "ERROR"  : style.RED,
    "REQUEST": style.MAGENTA,
}

LOG_NAME_MAX_LEN = max([len(x) for x in LOG_COLOR])

# make sure to have a system call when importing this file to allow color printing
os.system("")

def __log__(level, *args, **kwargs):
    """ Wrapper around print system function """
    header = "[" + str(level).rjust(LOG_NAME_MAX_LEN) + "]"
    # check if system can use ANSI color
    if sys.stdout.isatty():
        return print(LOG_COLOR[level], style.BOLD, header, style.RESET, *args, **kwargs)
    else:
        return print(header, *args, **kwargs)

def Debug(*args, **kwargs):
    """ Pretty printer of debug messages """
    return __log__("DEBUG", *args, **kwargs)

def Info(*args, **kwargs):
    """ Pretty printer of info messages """
    return __log__("INFO", *args, **kwargs)

def Error(*args, **kwargs):
    """ Pretty printer of error messages """
    return __log__("ERROR", *args, **kwargs)

def Warning(*args, **kwargs):
    """ Pretty printer of warning messages """
    return __log__("WARNING", *args, **kwargs)

def Request(*args, **kwargs):
    """ Pretty printer of request messages """
    return __log__("REQUEST", *args, **kwargs)