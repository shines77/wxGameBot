#!/usr/bin/python
# coding: utf-8

from enum import unique, Enum, IntEnum
import str

@unique
class LogType(IntEnum):
    OFF = 0
    DEFAULT = 1
    INFO = 2
    WARNING = 3
    VERBO = 4
    TRACE = 5
    DEBUG = 6
    ERROR = 7
    FATAL = 8
    CRITICAL = 9
    ALL = 10

class Console:
    def __init__(self, level = LogType.WARNING):
        self.level = level

    def join_text(self, log_type, *args):
        text = log_type
        i = 0
        for (arg,) in args:
            i += 1
            if i < len(args):
                text += str(arg) + ' '
            else:
                text += str(arg)
        return text

    def print(self, *args):
        if self.level.value >= LogType.DEFAULT.value:
            text = self.join_text('', args)
            print(text)

    def log(self, *args):
        if self.level.value >= LogType.DEFAULT.value:
            text = self.join_text("[Default] ", args)
            print(text)

    def info(self, *args):
        if self.level.value >= LogType.INFO.value:
            text = self.join_text("[Info] ", args)
            print(text)

    def warn(self, *args):
        if self.level.value >= LogType.WARNING.value:
            text = self.join_text("[Warning] ", args)
            print(text)

    def verbo(self, *args):
        if self.level.value >= LogType.VERBO.value:
            text = self.join_text("[Verbo] ", args)
            print(text)

    def trace(self, *args):
        if self.level.value >= LogType.TRACE.value:
            text = self.join_text("[Trace] ", args)
            print(text)

    def debug(self, *args):
        if self.level.value >= LogType.DEBUG.value:
            text = self.join_text("[Debug] ", args)
            print(text)

    def error(self, *args):
        if self.level.value >= LogType.ERROR.value:
            text = self.join_text("[Error] ", args)
            print(text)

    def fatal(self, *args):
        if self.level.value >= LogType.FATAL.value:
            text = self.join_text("[Fatal] ", args)
            print(text)

    def critical(self, *args):
        if self.level.value >= LogType.CRITICAL.value:
            text = self.join_text("[Critical] ", args)
            print(text)

    def nothing(self, *args):
        if self.level.value > LogType.ALL.value:
            text = self.join_text("[Nothing] ", args)
            print(text)
