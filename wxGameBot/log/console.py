#!/usr/bin/python
# coding: utf-8

from enum import unique, Enum, IntEnum

@unique
class LogLevel(IntEnum):
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

_inited = False
_loglevel = LogLevel.DEFAULT

_levelToName = {
    LogLevel.OFF: 'OFF',
    LogLevel.DEFAULT: 'DEFAULT',
    LogLevel.INFO: 'INFO',
    LogLevel.WARNING: 'WARNING',
    LogLevel.VERBO: 'VERBO',
    LogLevel.TRACE: 'TRACE',
    LogLevel.DEBUG: 'DEBUG',
    LogLevel.ERROR: 'ERROR',
    LogLevel.FATAL: 'FATAL',
    LogLevel.CRITICAL: 'CRITICAL',    
    LogLevel.ALL: 'ALL'
}

_nameToLevel = {
    'OFF': LogLevel.OFF,
    'DEFAULT': LogLevel.DEFAULT,
    'INFO': LogLevel.INFO,
    'WARN': LogLevel.WARNING,
    'WARNING': LogLevel.WARNING,
    'VERBO': LogLevel.VERBO,
    'TRACE': LogLevel.TRACE,
    'DEBUG': LogLevel.DEBUG,
    'ERROR': LogLevel.ERROR,
    'FATAL': LogLevel.FATAL,
    'CRITICAL': LogLevel.CRITICAL,    
    'ALL': LogLevel.ALL,
    'NOTSET': LogLevel.DEFAULT
}

def join_text(log_type, *args):
    text = log_type
    i = 0
    for (arg,) in args:
        i += 1
        if i < len(args):
            text += str(arg) + ' '
        else:
            text += str(arg)
    return text

class console(object):
    def __init__(self, level = LogLevel.INFO):
        global _inited
        global _loglevel
        print("console::__init__()")
        console.init(level)

    @staticmethod
    def init(level = LogLevel.INFO):
        global _inited
        if not _inited:
            console.set_level(level)
            _inited = True            

    @staticmethod
    def inited():
        global _inited
        return _inited

    @staticmethod
    def get_level():
        global _loglevel
        return _loglevel

    @staticmethod
    def get_level_name():
        global _loglevel
        global _levelToName
        if _loglevel in _levelToName:
            return _levelToName[_loglevel]
        else:
            return "INFO"

    @staticmethod
    def set_level(level = LogLevel.INFO):
        global _loglevel
        _loglevel = level

    @staticmethod
    def set_level_name(level_name = 'INFO'):
        global _loglevel
        global _nameToLevel
        # print("console::set_level_name(): level_name = " + str(level_name))
        level = LogLevel.OFF
        if level_name in _nameToLevel:
            level = _nameToLevel[level_name]
        else:
            level = LogLevel.INFO
        _loglevel = level
        return level

    @staticmethod
    def print(*args):
        global _loglevel
        if _loglevel.value >= LogLevel.DEFAULT.value:
            text = join_text('', args)
            print(text)

    @staticmethod
    def log(*args):
        global _loglevel
        if _loglevel.value >= LogLevel.DEFAULT.value:
            text = join_text("[Default] ", args)
            print(text)

    @staticmethod
    def info(*args):
        global _loglevel
        if _loglevel.value >= LogLevel.INFO.value:
            text = join_text("[Info] ", args)
            print(text)

    @staticmethod
    def warn(*args):
        global _loglevel
        if _loglevel.value >= LogLevel.WARNING.value:
            text = join_text("[Warning] ", args)
            print(text)

    @staticmethod
    def verbo(*args):
        global _loglevel
        if _loglevel.value >= LogLevel.VERBO.value:
            text = join_text("[Verbo] ", args)
            print(text)

    @staticmethod
    def trace(*args):
        global _loglevel
        if _loglevel.value >= LogLevel.TRACE.value:
            text = join_text("[Trace] ", args)
            print(text)

    @staticmethod
    def debug(*args):
        global _loglevel
        if _loglevel.value >= LogLevel.DEBUG.value:
            text = join_text("[Debug] ", args)
            print(text)

    @staticmethod
    def error(*args):
        global _loglevel
        if _loglevel.value >= LogLevel.ERROR.value:
            text = join_text("[Error] ", args)
            print(text)

    @staticmethod
    def fatal(*args):
        global _loglevel
        if _loglevel.value >= LogLevel.FATAL.value:
            text = join_text("[Fatal] ", args)
            print(text)

    @staticmethod
    def critical(*args):
        global _loglevel
        if _loglevel.value >= LogLevel.CRITICAL.value:
            text = join_text("[Critical] ", args)
            print(text)

    @staticmethod
    def nothing(*args):
        global _loglevel
        if _loglevel.value > LogLevel.ALL.value:
            text = join_text("[Nothing] ", args)
            print(text)

class Logger(object):
    def __init__(self, level = LogLevel.INFO):
        self.level = level

    def get_level(self):
        return self.level

    def set_level(self, level = LogLevel.INFO):
        self.level = level

    def print(self, *args):
        if self.level.value >= LogLevel.DEFAULT.value:
            text = join_text('', args)
            print(text)

    def log(self, *args):
        if self.level.value >= LogLevel.DEFAULT.value:
            text = join_text("[Default] ", args)
            print(text)

    def info(self, *args):
        if self.level.value >= LogLevel.INFO.value:
            text = join_text("[Info] ", args)
            print(text)

    def warn(self, *args):
        if self.level.value >= LogLevel.WARNING.value:
            text = join_text("[Warning] ", args)
            print(text)

    def verbo(self, *args):
        if self.level.value >= LogLevel.VERBO.value:
            text = join_text("[Verbo] ", args)
            print(text)

    def trace(self, *args):
        if self.level.value >= LogLevel.TRACE.value:
            text = join_text("[Trace] ", args)
            print(text)

    def debug(self, *args):
        if self.level.value >= LogLevel.DEBUG.value:
            text = join_text("[Debug] ", args)
            print(text)

    def error(self, *args):
        if self.level.value >= LogLevel.ERROR.value:
            text = join_text("[Error] ", args)
            print(text)

    def fatal(self, *args):
        if self.level.value >= LogLevel.FATAL.value:
            text = join_text("[Fatal] ", args)
            print(text)

    def critical(self, *args):
        if self.level.value >= LogLevel.CRITICAL.value:
            text = join_text("[Critical] ", args)
            print(text)

    def nothing(self, *args):
        if self.level.value > LogLevel.ALL.value:
            text = join_text("[Nothing] ", args)
            print(text)
