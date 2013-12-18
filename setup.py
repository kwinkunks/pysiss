#!/usr/bin/env python
""" file: setup.pyb (pyboreholes)
    author: Jess Robertson, CSIRO Earth Science and Resource Engineering
    date: Wednesday 1 May, 2013

    description: Distutils installer script for pyboreholes.
"""

import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup, find_packages

## VERSION NUMBERS
# Patch disutils if it can't cope with the 'classifiers' or 'download_url'
# keywords (for Python < 2.2.3)
from sys import version
if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

## PACKAGE INFORMATION
setup(
    name='pyboreholes',
    version='0.1.3a',
    description='Python functions for analysing borehole data',
    long_description=open('README.md').read(),
    author='Jess Robertson',
    author_email='jesse.robertson@csiro.au',
    url='http://bitbucket.org/jessrobertson/pyboreholes',
    packages=find_packages(),
    requires=['numpy', 'matplotlib'],
    extras_require={
        "continuous_wavelets": ['cwavelets'],
        "discrete_wavelets": ['pywavelets'],
        "machine_learning": ['sklearn']
    },
    ext_modules=[],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Geology',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
