#!/home/tops/bin/python

import os, sys ,re,string
import process
import configuration
from mako.template import Template
from currencychart import CurrencyChart


class WebGallery:
    def __init__(self, config = configuration.Configuration()):
        self.wmap       = config.webgallery_map
        self.wpath      = config.webgallerypath
        self.wfullpath  = "%s/images/full" % self.wpath
        self.wthumbpath = "%s/images/thumb" % self.wpath
        return


    def update(self):
        for item in self.wmap.keys():
            cname,tf = item.split('_')
            c = CurrencyChart(cname,tf)
            cp_full_cmd  = "cp -avf %s %s/%s.gif" % (c.get_latest_gif(), self.wfullpath, self.wmap[item])
            cp_thumb_cmd = "cp -avf %s %s/%s.gif" % (c.get_latest_gif(), self.wthumbpath, self.wmap[item])
            p = process.Process(cp_full_cmd)
            p.runInConsole()
            p = process.Process(cp_thumb_cmd)
            p.runInConsole()
        return 

    def build(self):
        context = dict()
        context['site'] = 'www.17forex.com'
        t = Template(filename = '/tmp/g.tpl')
        print t.render(**context)


if __name__ == '__main__':
    g = WebGallery()
    g.update()
    g.build()
        

    
