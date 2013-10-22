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
    description='Automatize sysadmin tasks, elegantly adaptable and scalable, Supports for dependency installing, environment profilling, Django+uWsgi+Nginx deployment, or adapt your own.',
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
    ],
    license="BSD",
    zip_safe=False,
    keywords='velvet_fabric',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)