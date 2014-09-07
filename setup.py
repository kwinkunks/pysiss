#!/usr/bin/env python
""" file: setup.py (pysiss)
    author: Jess Robertson, CSIRO Earth Science and Resource Engineering
    date: Wednesday 1 May, 2013

    description: Setuptools installer script for pysiss.
"""

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

# Get requirements from requirements.txt file
with open('requirements.txt') as fhandle:
    REQUIREMENTS = map(lambda l: l.strip('\n'), fhandle.readlines())

## PACKAGE INFORMATION
setup(
    # Metadata
    name='pysiss',
    version='0.0.2a',
    description='A pythonic interface to Spatial Information Services Stack '
                '(SISS) services',
    long_description=open('README.rst').readlines(),
    author='Jess Robertson',
    author_email='jesse.robertson@csiro.au',
    url='http://github.com/pysiss/pysiss',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: XML'
    ],

    # Dependencies
    install_requires=[
        'matplotlib>=1.0',
        'numpy>=1.6',
        'scipy>=0.9',
        'OWSLib>=0.8',
        'lxml',
        'simplejson>=3.0',
        'pandas>=0.10',
        'shapely',
        'requests',
    ],

    # Contents
    packages=find_packages(exclude=['test*']),
    package_data={
        'pysiss.vocabulary.resources': ['*']
    },
    test_suite='tests'
)
