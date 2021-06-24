#!/usr/bin/env python3

from satdb import BaseConfig

class STConfig(BaseConfig):
    def __init__(self, configfilename):
        self.node = 'spacetrack'
        self.configdic = {
                'user': 'user',
                'password': 'secret'
                }
        super().__init__(configfilename)

