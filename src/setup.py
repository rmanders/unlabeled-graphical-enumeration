#!/usr/bin/env python

from setuptools import setup, find_packages

requires = [
    'pillow',
    ]

setup(name='unlabeled-graph-enum',
      version='1.0',
      description='Generates all unlabeled graphs over n-vertices',
      author='Ryan Anderson',
      url='https://github.com/rmanders/unlabeled-graphical-enumeration',
      packages=['unlabeled']
      )

