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
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'wxGameBot = wxGameBot.utils:shell_entry'
        ]
    },
    install_requires=[
        'wxpy==0.3.9.8',
        'requests',
        'future',
    ],
    tests_require=[
        'pytest',
    ],
    url='https://github.com/shines77/wxGameBot',
    license='MIT',
    author='shines77',
    author_email='gz_shines@msn.com',
    description='微信游戏机器人',
    long_description=readme,
    keywords=[
        '微信',
        'WeChat',
        '游戏机器人'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'Topic :: Communications :: Chat',
        'Topic :: Utilities',
    ]
)
