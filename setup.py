#!/usr/bin/python
# coding: utf-8
# from __future__ import unicode_literals

import re
import codecs

from setuptools import find_packages, setup

with codecs.open('wxGameBot/__init__.py', encoding='utf-8') as fp:
    version = re.search(r"__version__\s*=\s*'([\w\-.]+)'", fp.read()).group(1)

with codecs.open('README.md', encoding='utf-8') as fp:
    readme = fp.read()

setup(
    name='wxGameBot',
    version=version,

    author='shines77',
    author_email='gz_shines@msn.com',
    url='https://github.com/shines77/wxGameBot',
    license='MIT',

    description='微信游戏机器人',
    long_description=readme,

    keywords=[
        '微信',
        'WeChat',
        'GameBot',
        '游戏机器人'
    ],

    entry_points={
        'console_scripts': [
            'wxGameBot = wxGameBot:console_entry'
        ]
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Communications :: Chat',
        'Topic :: Utilities',
    ],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    include_package_data=True,

    install_requires=[
        'wxpy==0.3.9.8',
        'requests',
        'future',
    ],

    tests_require=[
        'pytest',
    ],

    # List additional groups of dependencies here
    extras_require={},
)
