#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os

# from setuptools import setup, find_packages
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


# Package meta-data.
NAME = 'code_analyzer'
DESCRIPTION = 'Get most common words from your code.'
URL = 'https://github.com/draihal/code_analyzer'
EMAIL = 'draihal@gmail.com'
AUTHOR = 'draihal'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.0.2'
REQUIRED = [
    'nltk ~= 3.4.4',
]

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    license="MIT",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    install_requires=REQUIRED,
    packages=find_packages(),
    test_suite='tests',
    include_package_data=True,
)
