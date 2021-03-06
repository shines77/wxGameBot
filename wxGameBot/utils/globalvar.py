#!/usr/bin/python
# coding: utf-8

import logging, json
import traceback

_inited = False
_dict = {}

"""
try:
    # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
"""

"""

标题：python 跨文件之间的全局变量传参
See: https://www.jianshu.com/p/6cee728f3490

"""

class globalvar(object):
    def __init__(self):
        global _inited
        global _dict        
        # print("globalvar::__init__()")
        globalvar.init()

    @staticmethod
    def init():
        global _inited
        global _dict
        # print("globalvar::init()")
        if not _inited:
            _dict = {}
            _inited = True

    @staticmethod
    def inited():
        global _inited
        return _inited

    @staticmethod
    def clear():
        global _dict
        _dict = {}

    @staticmethod
    def find(key):
        global _dict
        if key in _dict:
            return True
        else:
            return False

    @staticmethod
    def get(key, defValue=None):
        global _dict
        try:
            # print("GlobalVar::get(): key = " + str(key))
            if key in _dict:
                return _dict[key]
            else:
                return 'Null_'
        except KeyError:
            # print("GlobalVar::get(): KeyError")
            return defValue
        except BaseException as err:
            # print("GlobalVar::get(): BaseException")
            logging.error(err)
            raise err

    @staticmethod
    def get_vars(*keys):
        global _dict
        try:
            if (len(keys) == 1) and (keys[0] == 'all'):
                dict = _dict
                return dict
            else:
                dict = {}
                for key in keys:
                    value = _dict[key]
                    dict[key] = value
                    logging.debug("GlobalVar::get_vars(): key = " + str(key) + ", value = " + str(value))
                return dict
        except BaseException as err:
            # print("GlobalVar::get_vars(): BaseException")
            logging.error(err)
            raise err

    @staticmethod
    def set(key, value):
        global _dict
        try:
            # print("GlobalVar::set(): key = " + str(key) + ", value = " + str(value))
            if isinstance(value, dict):
                value = json.dumps(value)
            _dict[key] = value
            logging.debug("GlobalVar::set_var(): key = " + str(key) + ", value = " + str(value))
        except BaseException as err:
            # print("GlobalVar::set(): BaseException")
            logging.error(err)
            raise err

    @staticmethod
    def set_vars(**kv_pairs):
        global _dict
        try:
            for key, value in kv_pairs.items():
                _dict[key] = value
                logging.debug("GlobalVar::set_vars(): key = " + str(key) + ", value = " + str(value))
        except BaseException as err:
            # print("GlobalVar::set_vars(): BaseException")
            logging.error(err)
            raise err

    @staticmethod
    def delete(key):
        global _dict
        try:
            del _dict[key]
            return True
        except KeyError:
            # print("GlobalVar::delete_var(): KeyError")
            logging.error("GlobalVar::delete(): key = " + str(key) + ", Error: key 不存在!")
            return False
