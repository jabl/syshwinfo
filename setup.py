#!/usr/bin/python

from distutils.core import setup
from fnmatch import fnmatch
import os

scripts = []
for file in os.listdir('.'):
    if fnmatch(file, '*.py') or fnmatch(file, '*.cgi'):
        scripts.append(file)
scripts.remove('setup.py')
print scripts

setup(name='syshwinfo',
      version='2009.1',
      description='Utilities for gathering system information and sending them to a central server.',
      author='Janne Blomqvist',
      author_email='Janne.Blomqvist@tkk.fi',
      license = 'GPLv3',
      url='http://www.fyslab.hut.fi/~/job/',
      scripts = scripts
     )

