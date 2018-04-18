#!/usr/bin/env python3
# coding: utf-8

import logging
import sys

from .main.bot import Bot
from .__main__ import console_entry

__title__ = 'wxGameBot'
__version__ = '0.1.0.0'
__author__ = 'shines77'
__license__ = 'MIT'
__copyright__ = '2018, shines77'

version_details = 'wxGameBot {ver} from {path} (python {pv.major}.{pv.minor}.{pv.micro})'.format(
    ver=__version__, path=__path__[0], pv=sys.version_info)

try:
    # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
