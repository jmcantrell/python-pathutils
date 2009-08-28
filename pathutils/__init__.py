import os.path

def condense(path):
    return path.replace(os.path.expanduser('~'), '~')

def expand(path):
    return os.path.abspath(os.path.expanduser(path))
