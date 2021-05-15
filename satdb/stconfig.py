#!/usr/bin/env python3

import yaml

#------------------------------------------------------------------------------
# Class for Space-Track configuration
class STConfig:
    def __init__(self, configfilename):
        self.configfilename = configfilename
        self.user = None
        self.password = None
        self.configdic = {'user': 'mysqluser',
                'password': 'secret'}
        self.config_read()
        self.set_configattributs()

    def config_read(self):
        configlist = []
        try:
            with open(self.configfilename, "r") as configfile:
#                for line in configfile:
#                    if line[0] != '#' and line[0] != '\n':
#                        configlist.append(line.strip('\n').split('='))
                configlist = yaml.load(configfile, Loader=yaml.FullLoader)["spacetrack"]

        except (IndexError, FileNotFoundError):
            print("Error opening file. Exiting.")
            exit()

        for configitem in configlist:
#            if configitem[0] in self.configdic.keys():
#                self.configdic[configitem[0]] = configitem[1].strip('"')
#            else:
#                print('Unknown configitemn: ', configitem[0])
            if configitem in self.configdic.keys():
                self.configdic[configitem] = configlist[configitem]
            else:
                print('Unknown configitemn: ', configitem)

    def print(self):
        print('Current config:')
        for configitem in self.configdic.keys():
            print("{:30} {}".format(configitem, self.configdic[configitem]))

    def set_configattributs(self):
        for key, value in self.configdic.items():
            setattr(self, key, value)

