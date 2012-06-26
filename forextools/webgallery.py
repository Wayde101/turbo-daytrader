#!/home/tops/bin/python

import os, sys ,re,string
import process
import configuration
from mako.template import Template
from currencychart import CurrencyChart


class WebGallery:
    def __init__(self, config = configuration.Configuration()):
        self.wmap       = dict()
        self.wpath      = config.webgallerypath
        self.wfullpath  = "%s/images/full" % self.wpath
        self.wthumbpath = "%s/images/thumb" % self.wpath
        self.t_row      = config.timeframe_row
        self.c_col      = config.currency_col
        self.tpl_file   = config.webgallerytpl
        self.out_file   = config.webgalleryout
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

    def expand(self):
        total_num = len(self.t_row) * len(self.c_col)
        a=self.wmap
        
        OUT_str=''
        for i in range(1, total_num + 1):
            OUT_str = OUT_str + "<li><a href=\"images/full/%0.3d.gif\"><img src=\"images/thumb/%0.3d.gif\" alt=\"%s\" /></a></li>\n" % (i,i,dict(zip(a.itervalues(), a.iterkeys()))["%0.3d" % i])

        return OUT_str

    def build(self,**kargs):
        idx = 1
        if kargs.has_key('t_row'):
            self.t_row = kargs['t_row']
        if kargs.has_key('c_col'):
            self.c_col = kargs['c_col']
        if kargs.has_key('htmlfile'):
            self.out_file = kargs['htmlfile']

        for c in self.c_col:
            for t in self.t_row:
                self.wmap[c + '_' + t] = '%0.3d' % idx
                idx = idx + 1

        self.update()

        context = dict()
        context['title']    = kargs['title'] if kargs.has_key('title') else 'ForexGallary'
        context['site']     = 'http://www.17forex.com'
        context['sitelogo'] =  'http://www.17forex.com/bbs/images/default/logo.gif'
        context['expand'] = self.expand
        t = Template(filename = self.tpl_file)
        f = open(self.out_file,'w')
        f.write(t.render(**context))
        f.close()


if __name__ == '__main__':
    g = WebGallery()
    #g.update()
    g.build(htmlfile='/home/yuting/src/3.0.5/examples/g.out.html',title='ForexGallary',t_row=['60','240','1440'],c_col=['eurusd','gbpusd'])
        

    
