#!/usr/bin/python
# coding: utf-8

from .main.shell import shell_entry
from .log.console import console, Logger, LogLevel
from .utils.globalvar import globalvar

def main():
    console.init(LogLevel.WARNING)
    globalvar.init()

    logger = Logger(LogLevel.WARNING)
    globalvar.set('logger', logger)

    # print("globalvar.inited() = " + str(globalvar.inited()))

    globalvar.set('test', '123')

    value = globalvar.get('test')
    print("value = " + str(value))

    console.log("console_main()")

def console_entry():
    main()
    shell_entry()

if __name__ == '__main__':
    console_entry()
