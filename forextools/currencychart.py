#!/home/tops/bin/python

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
        imgs.sort()
        return imgs[-1]

    def get_status(self):
        status = '%s/status.csv' % self.fullpath
        return status

    def dump_status(self):
        def splitLine(line):
            items = map(lambda x: tuple(x.strip().split('=')),
                        line.split(';'))
            return dict(items)
        
        content = list()
        items = dict()
        
        with open(self.get_status(), 'r') as f:
            content = f.xreadlines()
            content = map(lambda x: splitLine(x.strip()), content)
            for line in content:
                items[line['OBJNAME']] = line
            f.seek(0)
            f.close()
        return items

    def get_status_a(self):
        return

    def get_status_b(self):
        return 

if __name__ == '__main__':
    c = CurrencyChart("EURUSD","60")
    print c.dump_status()

