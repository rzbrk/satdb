#!/usr/bin/env python3

from setuptools import setup, find_package

setup(name = 'satdb',
        version = '0.1',
        author = 'Jan Grosser',
        author_email = 'email@jan-grosser.de',
#        license = '',
#        description = '',
#        long_description = open('README.md').read(),
        packages = find_packages(),
#        scripts = ['omm2db.py', 'st_dl_latest.py', 'tle2db.py'],
        install_requires = [
            'mysql-connector-python',
            'pyyaml',
            'spacetrack',
            'numpy',
            'TLE-tools',
            ]
        )
