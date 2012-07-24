#!/home/tops/bin/python

import os, sys ,re,string
import configuration
from mako.template import Template
from currencychart import CurrencyChart
from convert_wrapper import ConvertWrapper


class WebGallery:
    def __init__(self, config = configuration.Configuration()):
        self.ftpath    = '%s/forextools' % config.forexbase
        self.gbasedir   = '%s/html' % self.ftpath
        self.wmap       = dict()
        self.t_col      = config.timeframe_col
        self.c_row      = config.currency_row
        self.flip_list  = map(lambda x: x.upper(), config.currency_flip)
        return

    def init_gallery(self,gname):
        ghome    = "%s/%s" % (self.gbasedir,gname)
        if not os.path.exists(ghome):
            os.makedirs("%s/images/full"  % ghome )
            os.makedirs("%s/images/thumb" % ghome )
    
    def update(self,gname):
        for item in self.wmap.keys():
            cname,tf = item.split('_')
            flp = False
            c  = CurrencyChart(cname,tf)
            cp = ConvertWrapper()
            if cname.upper() in self.flip_list:
                flp = True
            cp.set_parm(text=item.replace('usd',''),flip=flp)
            cp.convert_copy(c.get_latest_gif() , "%s/%s/images/full/%s.gif" % (self.gbasedir, gname , self.wmap[item]))
            cp.convert_copy(c.get_latest_gif() , "%s/%s/images/thumb/%s.gif" % (self.gbasedir, gname , self.wmap[item]))
        return

    def expand(self):
        total_num = len(self.t_col) * len(self.c_row)
        a=self.wmap
        
        OUT_str=''
        for i in range(1, total_num + 1):
            OUT_str = OUT_str + "<li><a href=\"images/full/%0.3d.gif\"><img src=\"images/thumb/%0.3d.gif\" alt=\"%s\" /></a></li>\n" % (i,i,dict(zip(a.itervalues(), a.iterkeys()))["%0.3d" % i])

        return OUT_str


    def build(self,**kargs):
        idx   = 1
        g_title = kargs['title'] if kargs.has_key('title') else 'notitle'
        
        if kargs.has_key('t_col'):
            self.t_col = kargs['t_col']
        if kargs.has_key('c_row'):
            self.c_row = kargs['c_row']
            
        gallery_tpl      = "%s/tpl/gallery.tpl" % self.ftpath
        gallery_file     = "%s/%s/%s.html" % (self.gbasedir,g_title,'index')
        styles_css_tpl   = "%s/tpl/styles.css.tpl"% self.ftpath
        styles_css_file  = "%s/%s/styles.css" % (self.gbasedir,g_title)

        rpercent  = float(100) / float(len(self.t_col))

        for c in self.c_row:
            for t in self.t_col:
                self.wmap[c + '_' + t] = '%0.3d' % idx
                idx = idx + 1
        self.init_gallery(g_title)
        self.update(g_title)

        context = dict()
        context['title']    = kargs['title'] if kargs.has_key('title') else 'notitle'
        context['site']     = 'http://www.17forex.com'
        context['sitelogo'] = 'http://www.17forex.com/bbs/images/default/logo.gif'
        context['rpercent'] = "%.5f%%" % rpercent
        context['expand'] = self.expand
        gt = Template(filename = gallery_tpl)
        g = open(gallery_file,'w')
        g.write(gt.render(**context))
        g.close()
        
        st = Template(filename = styles_css_tpl)
        s = open(styles_css_file,'w')
        s.write(st.render(**context))
        s.close()


if __name__ == '__main__':
    g = WebGallery()
    g.build(title='ForexGallery_1h',t_col=['60','240','1440','10080','43200'],c_row=['SPTDXY','eurusd','gbpusd','usdchf','audusd','usdcad','usdjpy'])
    g.build(title='ForexGallery_5m',t_col=['5','15','60','240'],c_row=['SPTDXY','eurusd','gbpusd','usdchf','audusd','usdcad','usdjpy'])
