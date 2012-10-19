#!/home/tops/bin/python

import os, sys
import logging
import log
import process
import configuration

class ForexsysDb:
    def __init__(self, config = configuration.Configuration()):
        self.pg_dump  = config.pg_dump
        

    def backup(self, dst):
        bak_cmd = '%s -f %s' % (self.pg_dump,dst)

        p = process.Process(bak_cmd)
        p.runInConsole()
        return
        


