#!/usr/bin/env python

from setuptools import setup


# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(name='dt-suntime',
      version='1.0.0',
      description='Simple sunset and sunrise time calculation python library',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='DTBird&DTBat',
      url='https://github.com/DTBird-DTBat/suntime',
      copyright='Copyright 2024 SatAgro',
      license='LGPLv3',
      packages=['suntime'],
      install_requires=['python-dateutil'])
