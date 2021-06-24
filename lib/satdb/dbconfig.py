#!/usr/bin/env python3

from satdb import BaseConfig

class DBConfig(BaseConfig):
    def __init__(self, configfilename):
        self.node = 'satdb'
        self.configdic = {
                'host': 'localhost',
                'port': 3306,
                'database': 'spaceobjects',
                'user': 'mysqluser',
                'password': 'secret'
                }
        super().__init__(configfilename)

