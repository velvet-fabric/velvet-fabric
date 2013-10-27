#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='velvet_fabric',
    version='0.0.1',
    description='Dependency installing, virtualenv creator, automatize typical server tasks.',
    long_description=readme + '\n\n' + history,
    author='Enrique Paredes',
    author_email='enrique.iknite@gmail.com',
    url='https://github.com/iknite/velvet_fabric',
    packages=[
        'velvet_fabric',
    ],
    package_dir={'velvet_fabric': 'velvet_fabric'},
    include_package_data=True,
    install_requires=[
        'fabric>=1.8'
    ],
    license="BSD",
    zip_safe=False,
    keywords='velvet_fabric, fabric, django, install, nginx, uwsgi',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Clustering',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Systems Administration',
    ],
    test_suite='tests',
)
