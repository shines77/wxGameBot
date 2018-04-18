# coding: utf-8
from __future__ import unicode_literals

import inspect
import logging
import random
import re
import threading
import weakref
from functools import wraps

from wxGameBot.compatible import PY2

if PY2:
    from future.builtins import str

def start_new_thread(target, args=(), kwargs=None, daemon=True, use_caller_name=False):
    """
    启动一个新的进程，需要时自动为进程命名，并返回这个线程
    
    :param target: 调用目标
    :param args: 调用位置参数
    :param kwargs: 调用命名参数
    :param daemon: 作为守护进程
    :param use_caller_name: 为 True 则以调用者为名称，否则以目标为名称

    :return: 新的进程
    :rtype: threading.Thread
    """

    if use_caller_name:
        # 使用调用者的名称
        name = inspect.stack()[1][3]
    else:
        name = target.__name__

    logging.getLogger(
        # 使用外层的 logger
        inspect.currentframe().f_back.f_globals.get('__name__')
    ).debug('new thread: {}'.format(name))
    if PY2:
        _thread = threading.Thread(
            target=target, args=args, kwargs=kwargs,
            name=name)
        _thread.setDaemon(daemon)
    else:
        _thread = threading.Thread(
            target=target, args=args, kwargs=kwargs,
            name=name, daemon=daemon
        )
    _thread.start()

    return _thread
