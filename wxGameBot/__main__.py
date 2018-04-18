#!/usr/bin/python
# coding: utf-8

from .utils import shell_entry
from .log.console import Console, LogType
from .utils.globalvar import GlobalVar

if __name__ == '__main__':
    console = Console(LogType.WARNING)
    globalvar = GlobalVar()
    globalvar.set_var('console', console)

    print("globalvar.is_inited() = " + str(globalvar.is_inited()))

    globalvar.set_var('test', '123')

    value = globalvar.get_var('test')
    print("value = " + str(value))    

    shell_entry()
