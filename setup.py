#!/usr/bin/env python

from setuptools import setup, find_packages


setup(

    name='graphs-graph-enum',

    version='1.0',

    description='Generates all graphs graphs over n-vertices',

    author='Ryan Anderson',

    url='https://github.com/rmanders/graphs-graphical-enumeration',

    packages=find_packages(),

    install_requires=['pillow>=2.9.0'],

    entry_points={
        'console_scripts': [
            'genum=scripts.main:main',
        ],
    },
)

