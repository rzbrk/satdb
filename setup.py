#!/usr/bin/env python3

# install module/scripts with:
# python setup.py install

#from distutils.core import setup
from setuptools import setup

setup(name = 'satdb',
        version = '0.1',
        author = 'Jan Grosser',
        author_email = 'email@jan-grosser.de',
#        license = '',
#        description = '',
#        long_description = open('README.md').read(),
        packages = ['satdb'],
        scripts = ['omm2db.py', 'st_dl_latest.py'],
        install_requires = [
            'mysql-connector-python',
            'pyyaml',
            'spacetrack',
            'numpy',
            ]
        )
