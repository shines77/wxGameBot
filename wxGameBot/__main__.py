#!/usr/bin/python
# coding: utf-8

from .main.shell import shell_entry
from .log.console import Console, LogType
from .utils.globalvar import GlobalVar

def console_main():
    console = Console(LogType.WARNING)
    globalvar = GlobalVar()
    globalvar.set('console', console)

    # print("globalvar.inited() = " + str(globalvar.inited()))

    # globalvar.set('test', '123')

    # value = globalvar.get('test')
    # print("value = " + str(value))

def console_entry():
    console_main()
    shell_entry()

if __name__ == '__main__':
    console_entry()
