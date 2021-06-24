#!/usr/bin/env python3

import yaml

#------------------------------------------------------------------------------
# Base class for configuration
class BaseConfig:
    def __init__(self, configfilename):
        self.configfilename = configfilename

        try:
            self.node
        except:
            self.node = ''

        try:
            self.configdic
        except:
            self.configdic = []

        self._config_read()
        self._set_attr()

    def _config_read(self):
        configlist = []
        try:
            with open(self.configfilename, "r") as configfile:
                configlist = yaml.load(configfile, Loader=yaml.FullLoader)
                if not self.node == '':
                    configlist = configlist[self.node]

        except (IndexError, FileNotFoundError):
            print("Error opening file. Exiting.")
            exit()

        for configitem in configlist:
            if configitem in self.configdic.keys():
                self.configdic[configitem] = configlist[configitem]

    def print(self):
        print('Current config:')
        for configitem in self.configdic.keys():
            print("{:30} {}".format(configitem, self.configdic[configitem]))

    def _set_attr(self):
        for key, value in self.configdic.items():
            setattr(self, key, value)

