#!/home/tops/bin/python

import os, sys ,re,string
import time
from glob import glob
import configuration
from ft_utils import *

class CurrencyChart:
    def __init__(self, cur_name,cur_tf, config = configuration.Configuration()):
        self.cur_name      = cur_name.upper()
        self.tf            = cur_tf
        self.fullpath      = ''
        self.ccstr         = ''

        # some status keys define at below

        for path in config.mt4shotpath:
            p = '%s/%s_%s' % (path,self.cur_name,self.tf)
            if os.path.exists(p):
                self.fullpath = p
                #print "Found:", self.fullpath
                pass

        self.status_file   = '%s/status.csv' % self.fullpath
        self.status        = self.get_status();

        
    def get_latest_gif(self):
        imgs = glob('%s/*.gif' % self.fullpath)
        imgs.sort()
        ret = 'noimgs' if len(imgs) == 0 else imgs[-1]
        return ret
    
    def get_status(self):
        def splitLine(line):
            if re.search('OBJNAME=CC',line):
                self.ccstr = line
            items = map(lambda x: tuple(x.strip().split('=')),
                        line.split(';'))
            return dict(items)
        
        content = list()
        items = dict()
        
        with open(self.status_file, 'r') as f:
            content = f.xreadlines()
            content = map(lambda x: splitLine(x.strip()), content)
            for line in content:
                items[line['OBJNAME']] = line
            f.seek(0)
            f.close()
        return items

    def get_range_gifs_to_now(self,rg):
        time_range = read_time(rg)
        time_now   = time.time()
        time_from  = time_now - time_range
        gifs_ret   = []
        
        gifs = glob('%s/*.gif' % self.fullpath)

        for gif in gifs:
            p = re.compile('_\d+\/(\d+)\.gif$')
            c = int(p.search(gif).groups(1)[0])
            if time_from < c:
                gifs_ret.append(gif)
        return gifs_ret

    def get_out_of_range_gifs(self,rg):
        time_range = read_time(rg)
        time_now   = time.time()
        time_from  = time_now - time_range
        gifs_ret   = []
        
        gifs = glob('%s/*.gif' % self.fullpath)

        for gif in gifs:
            p = re.compile('_\d+\/(\d+)\.gif$')
            c = int(p.search(gif).groups(1)[0])
            if time_from > c:
                gifs_ret.append(gif)

        return gifs_ret


if __name__ == '__main__':
    c = CurrencyChart("EURUSD","60")
    print c.ccstr
    print c.get_status()
    #print c.get_range_gifs_to_now('2days')
    # print c.get_latest_gif()
    # print len(c.get_out_of_range_gifs('4days'))

