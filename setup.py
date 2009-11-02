#!/usr/bin/env python

from setuptools import setup

setup(
        name='PathUtils',
        version='0.8.0',
        description='Various small utilities for working with paths.',
        author='Jeremy Cantrell',
        author_email='jmcantrell@gmail.com',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Natural Language :: English',
            'Programming Language :: Python',
            ],
        entry_points={
            'console_scripts': [
                'pathtags=pathtags:main',
                ]
            },
        packages=[
            'pathutils',
            ],
        py_modules=[
            'pathtags',
            ],
        )
