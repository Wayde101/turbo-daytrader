#!/home/tops/bin/python

import os, sys
import logging
import log
import process
import configuration
import time

class ForexsysDb:
    def __init__(self, config = configuration.Configuration()):
        self.pg_dump   = config.pg_dump
        self.pg_backup = config.pg_backup
        self.db_user      = config.forexsys_user
        self.db_pass      = config.forexsys_db
        
        if not os.path.isdir(self.pg_backup):
            os.mkdir(self.pg_backup)
        

    def backup(self):
        tm_year,tm_mon,tm_mday,tm_hour,tm_min,tm_sec,tm_wday,tm_yday,tm_isdst=time.localtime()
        bak_file = '%s%s%s.dump' % (tm_year, 
                               tm_mon,
                               tm_mday)

        bak_cmd  = '%s -U %s %s -f %s/%s' % (self.pg_dump,
                                             self.db_user,
                                             self.db_pass,
                                             self.pg_backup,
                                             bak_file)

        p = process.Process(bak_cmd)
        p.runInConsole()
        return


# vim: ts=4 sw=4 ai et
