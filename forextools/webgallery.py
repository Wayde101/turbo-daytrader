#! /usr/bin/env python

import os, sys ,re,string
import process
import configuration
from currencychart import CurrencyChart


class WebGallery:
    def __init__(self, config = configuration.Configuration()):
        self.wmap = config.webgallery_map
        self.wpath = config.webgallerypath
        return


    def update(self):
        for item in self.wmap.keys():
            cname,tf = item.split('_')
            c = CurrencyChart(cname,tf)
            cp_full_cmd  = "cp -avf %s %s/full/%s.gif" % (c.get_latest_gif(), self.wpath, self.wmap[item])
            cp_thumb_cmd = "cp -avf %s %s/thumb/%s.gif" % (c.get_latest_gif(), self.wpath, self.wmap[item])
            p = process.Process(cp_full_cmd)
            p.runInConsole()
            p = process.Process(cp_thumb_cmd)
            p.runInConsole()

        return 

if __name__ == '__main__':
    g = WebGallery()
    g.update()
        

    
