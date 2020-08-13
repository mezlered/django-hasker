from config.base import *

DEBUG = True

try:
    from config.local import *
except ImportError:
    pass
