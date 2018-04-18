
import sys, math
import traceback
from ..log.console import Console
from ..utils.globalvar import GlobalVar

globalvar = GlobalVar()
console = globalvar.get("console")

def display_exception(err):
    global console
    console.warn('=============================================================')
    # console.warn('str(Exception):        ', str(Exception))
    # console.warn('str(err):              ', str(err))
    # console.warn('repr(err):             ', repr(err))
    console.warn('traceback.print_exc(): ', traceback.print_exc())
    console.warn('traceback.format_exc():\n%s' % traceback.format_exc())
    console.warn('=============================================================')
