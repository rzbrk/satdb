#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name = 'satdb',
        packages = find_packages(),
        install_requires = [
            'mysql-connector-python',
            'pyyaml',
            'spacetrack',
            'numpy',
            'TLE-tools',
            ]
        )
