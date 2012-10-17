#!/home/tops/bin/python

import os, sys ,re,string
import configuration
from currencychart import CurrencyChart
from convert_wrapper import ConvertWrapper

class GifGallery:
    def __init__(self,cur_name,cur_tf,config = configuration.Configuration()):
        self.ftpath    = '/home/yuting/project/turbo-daytrader/forextools'
        self.gbasedir   = '%s/html' % self.ftpath
        self.wmap       = dict()
        self.flip_list  = map(lambda x: x.upper(), config.currency_flip)
        self.chart      = CurrencyChart(cur_name,cur_tf)
        
    def build_moving_gifs(self,rg):
        c = ConvertWrapper()
        c.convert_delay(1,self.chart.get_range_gifs_to_now(rg),'/tmp/7day.gif')

    def build_mpeg(self,rg):
        c = ConvertWrapper()
        c.ffmpeg_prepare(self.chart.get_range_gifs_to_now(rg),'/tmp/a.gif')

if __name__ == '__main__':
    g = GifGallery('eurusd','60')
    #g.build_moving_gifs('7day')
    g.build_mpeg('1day')

