#!/home/tops/bin/python

import os, sys ,re,string
import time
from glob import glob
import configuration
from currencychart import CurrencyChart
from ft_utils import *

class CurrencyStatus:
    def __init__(self, cur_name,cur_tf, config = configuration.Configuration()):
        self.cur_name      = cur_name.upper()
        self.tf            = cur_tf
        self.chart         = CurrencyChart(cur_name,cur_tf)
        self.status        = self.chart.get_status()
        self.flip_list     = map(lambda x: x.upper(), config.currency_flip)
        self.cc_cache      = '%s/cc/%s_%s' % (config.forexbase, \
                                              self.cur_name, \
                                              self.tf)
        self.cache_status = dict()
        
    def has_cc(self):
        if self.status['CC'].has_key('CCDIST'):
            return True
        else:
            return False

    def get_CC_keys(self):
        return self.status['CC'].keys()

    def get_CC_value(self,key):
        if self.status['CC'].has_key(key):
            return self.status['CC'][key]
        else:
            print "CC does not have %s" % key
            return 'NA'

    def get_MW_keys(self):
        return self.status['MW'].keys()
        

    def get_MW_value(self,key):
        if self.status['MW'].has_key(key):
            return self.status['MW'][key]
        else:
            print "MW does not have %s" % key
            return 'NA'

    def get_bid(self):
        return self.status['MarketInfo']['BID']
    
    def get_ask(self):
        return self.status['MarketInfo']['ASK']

        
    def get_MSYS_trend(self):
        flip      = -1 if self.cur_name.upper() in self.flip_list else 1
        ret_code  = 0
        if self.status['TrendSys']['M55'] > self.status['TrendSys']['M34'] and \
           self.status['TrendSys']['M55'] > self.status['TrendSys']['M34'] and \
           self.status['TrendSys']['M55'] > self.status['TrendSys']['M21'] and \
           self.status['TrendSys']['M55'] > self.status['TrendSys']['M13'] and \
           self.status['TrendSys']['M55'] > self.status['TrendSys']['M8'] and \
           self.status['TrendSys']['M55'] > self.status['TrendSys']['M5']:
            ret_code = -1 * flip

        if self.status['TrendSys']['M55'] < self.status['TrendSys']['M34'] and \
           self.status['TrendSys']['M55'] < self.status['TrendSys']['M34'] and \
           self.status['TrendSys']['M55'] < self.status['TrendSys']['M21'] and \
           self.status['TrendSys']['M55'] < self.status['TrendSys']['M13'] and \
           self.status['TrendSys']['M55'] < self.status['TrendSys']['M8'] and \
           self.status['TrendSys']['M55'] < self.status['TrendSys']['M5']:
            ret_code = 1 * flip
            
        return ret_code

    def get_MSYS_status(self):
        flip      = -1 if self.cur_name.upper() in self.flip_list else 1
        ret_code  = 0

        if self.status['TrendSys']['M55'] > self.status['TrendSys']['M34'] and \
           self.status['TrendSys']['M34'] > self.status['TrendSys']['M21'] and \
           self.status['TrendSys']['M21'] > self.status['TrendSys']['M13'] and \
           self.status['TrendSys']['M13'] > self.status['TrendSys']['M8'] and \
           self.status['TrendSys']['M8'] > self.status['TrendSys']['M5']:
            ret_code = -1 * flip

        if self.status['TrendSys']['M55'] < self.status['TrendSys']['M34'] and \
           self.status['TrendSys']['M34'] < self.status['TrendSys']['M21'] and \
           self.status['TrendSys']['M21'] < self.status['TrendSys']['M13'] and \
           self.status['TrendSys']['M13'] < self.status['TrendSys']['M8'] and \
           self.status['TrendSys']['M5'] < self.status['TrendSys']['M5']:
            ret_code = 1 * flip

        return ret_code

    def get_nearest_zpoint(self):
        ret_point = 0
        flip      = -1 if self.cur_name.upper() in self.flip_list else 1
        MW_up   = self.status['MW_up']['OBJPROP_TIME1']
        MW_down = self.status['MW_down']['OBJPROP_TIME1']
        
        ret_point = 1*flip if MW_up > MW_down else -1 * flip

        return ret_point

    def has_cc_cache(self):
        return os.path.exists(self.cc_cache)

    def load_cc_cache(self):
        if not self.has_cc_cache():
            return

        def splitLine(line):
            items = map(lambda x: tuple(x.strip().split('=')),
                        line.split(';'))
            return dict(items)
        
        content = list()
        self.cache_status = dict()
        
        with open(self.cc_cache, 'r') as f:
            content = f.xreadlines()
            content = map(lambda x: splitLine(x.strip()), content)
            for line in content:
                self.cache_status[line['OBJNAME']] = line
            f.seek(0)
            f.close()

    def cc_A_changed(self):
        if not self.has_cc():
            return False
        return self.status['CC']['OBJPROP_PRICE1'] != \
            self.cache_status['CC']['OBJPROP_PRICE1']

    def cc_B_changed(self):
        if not self.has_cc():
            return False
        return self.status['CC']['OBJPROP_PRICE2'] != \
            self.cache_status['CC']['OBJPROP_PRICE2']
    
    def cc_C_changed(self):
        if not self.has_cc():
            return False
        return self.status['CC']['OBJPROP_PRICE3'] != \
            self.cache_status['CC']['OBJPROP_PRICE3']


    def update_cc_cache(self):
        if self.has_cc():
            with open(self.cc_cache,'w') as f:
                f.write(self.chart.ccstr)
                f.close()
    
    
if __name__ == '__main__':
    conf      = configuration.Configuration()
    timeframe = ['60','240','1440','10080','43200']
    currency  = ['eurusd','gbpusd','usdchf','audusd','usdcad','usdjpy']
    
    c = CurrencyStatus('eurusd','60')
    c.load_cc_cache()
    print c.cache_status
    c.update_cc_cache()
