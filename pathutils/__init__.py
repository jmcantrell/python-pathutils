import os.path

def condense(path):
    return path.replace(os.path.expanduser('~'), '~')

def expand(path):
    return os.path.abspath(os.path.expanduser(path))

def relative(path, start=None):
    """Gets the path to 'dst' relative to 'src'.
    >>> relative('/usr/', '/usr/bin/')
    '..'
    >>> relative('/usr/local/bin/', '/usr/bin/')
    '../local/bin'
    >>> relative('/home/jeremy/bin/', '/home/jeremy/')
    'bin'
    >>> relative('/home/jeremy/lib/python/', '/home/jeremy/')
    'lib/python'
    >>> relative('/', '/')
    ''
    >>> relative('/', '/usr/bin/')
    '../../'
    """
    if not path: raise ValueError("Path not provided")
    if not start: start = os.getcwd()
    if start == path: return ''
    start_list = os.path.abspath(start).split(os.path.sep)
    path_list = os.path.abspath(path).split(os.path.sep)
    i = len(os.path.commonprefix([start_list, path_list]))
    rel_list = [os.path.pardir] * (len(start_list)-i) + path_list[i:]
    return os.path.join(*rel_list)

def add_sep(path):
    return path.rstrip(os.path.sep) + os.path.sep
