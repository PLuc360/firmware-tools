import argparse
import sys
import os

# add root directory to the path to be able to import modules
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from lib.Generic.GenericTypes import dir_path, file_path
from lib.Generic.Files import ListFiles
import lib.Generic.Logs as Logs

def __main__():
    """ Main function to manage code style check operations
    """

    # define argument parser
    parser = argparse.ArgumentParser(description='Manage code style check operations')
    parser.add_argument('-i', '--input', required=True, default=None, help='Input directory or file')
    parser.add_argument('-b', '--checker_bin', type=file_path, required=True, help='UNCRUSTIFY binary file path')
    parser.add_argument('-e', '--exclude', action='append', type=dir_path, default=[], help='Exclude directory(ies) from being processed')
    parser.add_argument('-c', '--config', type=file_path, help='Path to the uncrustify configuration file')
    parser.add_argument('--check', action='store_true', default=True, help='Use this option to only check files')
    parser.add_argument('--replace', action='store_true', default=False, help='Use this option to check and replace files')
    parser.add_argument('--recursive', action='store_true', default=False, help='Apply requested action on all input subdirectories')

    # parse arguments
    args = parser.parse_args()

    input_file = None
    input_dir  = None
    try:
        input_file = file_path(args.input)
    except FileNotFoundError:
        input_dir = dir_path(args.input)

    # replace command overwrites check command
    if args.replace and args.check:
        args.check = False

    # path/to/uncrustify
    cmd = os.path.abspath(args.checker_bin)

    # -c config_file.cfg
    cmd += ' -c ' + os.path.abspath(args.config)

    if args.check:
        cmd += ' --check '
    else:
        cmd += ' --replace --no-backup '

    # compute full path of args directories
    if len(args.exclude) != 0:
        args.exclude = [os.path.abspath(d) for d in args.exclude]
    if input_dir is not None:
        input_dir = os.path.abspath(input_dir)
    if input_file is not None:
        input_file = os.path.abspath(input_file)

     # compute file list for further processing
    if input_file is not None:
        if input_file.endswith(".c") or input_file.endswith(".h"):
            listingSuccess = True
            fileList = [input_file]
        else:
            listingSuccess = False
    else:
        listingSuccess, fileList = ListFiles(input_dir,
                                             extension_filter=['.c', '.h'],
                                             excluded_list=args.exclude,
                                             recursive=args.recursive)

    if not listingSuccess:
        Logs.Error("Could not find files to process in input directory {}".format(input_dir))
        return 1

    # add list of files to the command
    errorFileList = []
    for f in fileList:
        fileCmd = cmd + f
        result = os.system(fileCmd)
        if result != 0:
            errorFileList.append(f)

    Logs.Info('--- check_code_style result ---')
    Logs.Info('\tAction:  {}'.format('check' if args.check else 'replace'))
    Logs.Info('\tSuccess: {}/{}'.format(len(fileList) - len(errorFileList), len(fileList)))
    Logs.Info('\tError:   {}/{}'.format(len(errorFileList), len(fileList)))

    if (len(errorFileList) != 0):
        for f in errorFileList:
            Logs.Error('\t- {}'.format(f))

    return (len(errorFileList) != 0)

if __name__ == "__main__":
    # execute only if run as a script
    sys.exit(__main__())
