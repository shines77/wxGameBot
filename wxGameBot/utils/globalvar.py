#!/usr/bin/python
# coding: utf-8

import log, str
import Exception, KeyError
import traceback

global _dict
_dict = {}

class GlobalVar():
    def __init__(self):
        global _dict

    def get_var(self, key, defValue=None):
        try:
            return _dict[key]
        except KeyError:
            return defValue
        except BaseException as err:
            log.error(err)
            raise err

    def get_vars(self, *keys):
        try:
            dict = {}
            if len(keys) == 1:
                if keys[0] == 'all':
                    dict = _dict
                else:
                    for key in keys:
                        value = _dict[key]
                        dict[key] = value
                        log.debug("GlobalVar::get_vars(): key = " + str(key) + ", value = " + str(value))
            else:
                for key in keys:
                    value = _dict[key]
                    dict[key] = value
                    log.debug("GlobalVar::get_vars(): key = " + str(key) + ", value = " + str(value))

            return dict
        except BaseException as err:
            log.error(err)
            raise err

    def set_var(self, key, value):
        try:
            _dict[key] = value
            log.debug("GlobalVar::set_var(): key = " + str(key) + ", value = " + str(value))
        except BaseException as err:
            log.error(err)
            raise err

    def set_vars(self, **kv_pairs):
        try:
            for key, value in kv_pairs.items():
                _dict[key] = value
                log.debug("GlobalVar::set_vars(): key = " + str(key) + ", value = " + str(value))
        except BaseException as err:
            log.error(err)
            raise err

    def delete_var(self, key):
        try:
            del _dict[key]
            return _dict
        except KeyError:
            log.error("GlobalVar::delete_var(): key = " + str(key) + ", Error: key 不存在!")
  