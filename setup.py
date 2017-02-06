#!/usr/bin/env python

from distutils.core import setup

setup(
    name='txpoloniex',
    version='0.1',
    description='Minimalist Twisted wrapper for the Poloniex API',
    author='Daniel Walsh',
    author_email='459dan@gmail.com',
    packages=['txpoloniex'],
    install_requires=[
        'txaio>=2.6.0',
        'Twisted>=16.6.0',
    ],
)
