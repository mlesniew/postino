#!/usr/bin/env python3
# coding: utf-8

import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name='postino',
    version='0.3',
    description='Easy email sending',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/mlesniew/postino',
    author='Michał Leśniewski',
    author_email='mlesniew@gmail.com',
    license='GPLv3',
    packages=['postino'],
    test_suite='test',
    entry_points={
        'console_scripts': ['postino=postino.__main__:main'],
        },
    python_requires='>=3.0'
    )
