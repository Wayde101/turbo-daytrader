#! /usr/bin/env python

import os, sys ,re,string
from glob import glob
import configuration



class CurrencyChart:
    def __init__(self, cur_name,cur_tf, config = configuration.Configuration()):
        self.cur_name      = cur_name.upper()
        self.tf            = cur_tf
        self.fullpath      = ''
        # some status keys define at below

        for path in config.mt4shotpath:
            p = '%s/%s_%s' % (path,self.cur_name,self.tf)
            if os.path.exists(p):
                self.fullpath = p
                print "Found:", self.fullpath
                pass

        return
        
    def get_latest_gif(self):
        imgs = glob('%s/*.gif' % self.fullpath)
        imgs.sort();
        return imgs[-1]

    def get_status(self):
        status = '%s/status.csv' % self.fullpath
        return status

    def load_status(self):
        #from juehai
        return

    def get_status_a(self):
        return

    def get_status_b(self):
        return 

if __name__ == '__main__':
    c = CurrencyChart("EURUSD","60")
    print c.get_latest_gif()
    print c.get_status()

