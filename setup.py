#!/usr/bin/env python

from setuptools import setup, find_packages
from glob import glob

setup(
        name='PathUtils',
        version='0.6.2',
        description='Various small utilities for working with paths.',
        author='Jeremy Cantrell',
        author_email='jmcantrell@gmail.com',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Natural Language :: English',
            'Programming Language :: Python',
            ],
        packages=[
            'pathutils',
            ],
        )
