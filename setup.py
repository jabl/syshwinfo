#!/usr/bin/python

from distutils.core import setup
from glob import glob

# Scripts whose names end in a-z or 1-9 (avoids emacs backup files)
scripts = glob('scripts/*[a-z,1-9]')

setup(name='syshwinfo',
      version='2.0',
      description='Utilities for gathering system information and sending them to a central server.',
      author='Janne Blomqvist',
      author_email='Janne.Blomqvist@aalto.fi',
      license = 'MIT',
      url='https://github.com/jabl/syshwinfo',
      scripts = scripts
     )

