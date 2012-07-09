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

    
if __name__ == '__main__':
    conf      = configuration.Configuration()
    timeframe = ['60','240','1440','10080','43200']
    currency  = ['eurusd','gbpusd','usdchf','audusd','usdcad','usdjpy']
    
    for tf in timeframe:
        c = CurrencyStatus("SPTDXY",tf)
        print tf
        print c.get_nearest_zpoint()
        print c.get_MSYS_trend()
        
    
    c = CurrencyStatus("USDCHF","15")
    # print c.status
    # print c.get_CC_keys()
    # print c.get_CC_value("CCDIST")
    # print c.get_MW_keys()
    # print c.get_MW_value("atr55")
    print c.get_nearest_zpoint()
    
