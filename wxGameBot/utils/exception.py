
import sys, math
import traceback
from ..log.console import console, Logger, LogLevel
from ..utils.globalvar import globalvar

logger = globalvar.get("logger")

def display_exception(err):
    global logger
    console.warn('=============================================================')
    # console.warn('str(Exception):        ', str(Exception))
    # console.warn('str(err):              ', str(err))
    # console.warn('repr(err):             ', repr(err))
    console.warn('traceback.print_exc(): ', traceback.print_exc())
    console.warn('traceback.format_exc():\n%s' % traceback.format_exc())
    console.warn('=============================================================')
