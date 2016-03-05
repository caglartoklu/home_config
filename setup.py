#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
setup.py for home_config.

pip setup.py install
pip setup.py test
"""

# pylint: disable=C0103
# Disables:
# Invalid module name "atom-linter_xxxxxx"at
# line 1 col 1 in dropshadow_bed\__init__.py
# This warning occurs in linter-pylint extension of Atom.

import os
from setuptools import setup

NAME = 'home_config'
VERSION = '0.1'
SHORT_DESC = """A library to easily create and prioritize the config files
for your application."""
URL = 'http://github.com/caglartoklu/home_config'
AUTHOR = 'Caglar Toklu'
AUTHOR_EMAIL = 'caglartoklu@gmail.com'


def read_adjacent_file_content(file_name):
    """
    Reads the contents of an adjacent file and returns it.
    """
    fhandle = open(os.path.join(os.path.dirname(__file__), file_name))
    content = fhandle.read()
    fhandle.close()
    return content


setup(name=NAME,
      version=VERSION,
      description=SHORT_DESC,
      long_description=read_adjacent_file_content('README.rst'),
      url=URL,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license='Apache',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Plugins',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development',
      ],
      keywords='home directory config',
      packages=['home_config'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
