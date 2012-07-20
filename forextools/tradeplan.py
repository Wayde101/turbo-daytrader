#!/home/tops/bin/python

import os, sys ,re,string
import time
from glob import glob
import configuration
from currencychart import CurrencyChart
from currencystatus import CurrencyStatus
from ticket import Ticket
from ft_utils import *


class TradePlan:
    def __init__(self,cur_name,cur_tf,config = configuration.Configuration()):
        self.cur_name           = cur_name.upper()
        self.cur_tf             = cur_tf
        self.flip_list          = map(lambda x: x.upper(), config.currency_flip)
        self.timeframes         = config.timeframe_list
        self.CS                 = CurrencyStatus(self.cur_name,cur_tf)
        self.CC                 = CurrencyChart(self.cur_name,cur_tf)
        self.ticket_in          = '%s/ticket.in' %  self.CC.fullpath

        pass


    def has_pending_ticket(self):
        print self.ticket_in
        ret = True if os.path.isfile(self.ticket_in) else False
        return ret
    
    # just a test
    def auto_cc_plan(self):
        status = self.CS.status
        ticket = Ticket(self.cur_name,self.cur_tf)
        if not self.CS.has_cc():
            return
        
        cmd      = 1 if status['CC']['ZPOINT'] == 'MW_down' else 0
        factor   = -1 if cmd ==  1 else 1
        entry    = float(status['CC']['CC1P']) 
        stoploss = float(status['CC']['CC1P']) + 0.10 * factor
        takeprofit= status['CC']['OBJPROP_PRICE1']

        ticket.new(ordertype = 'ordersend', orderbody = {'cmd':cmd,'vol':0.01,'price':entry,'stoploss':stoploss,'takeprofit':takeprofit})
        return


    def get_currency_effort(self):
        status = self.CS.status
        atr55   = float(status['MW']['atr55'])
        MW_up   = float(status['MW_up']['OBJPROP_PRICE1'])
        MW_up_t = float(status['MW_up']['OBJPROP_TIME1'])
        MW_down = float(status['MW_down']['OBJPROP_PRICE1'])
        MW_down_t = float(status['MW_down']['OBJPROP_TIME1'])

        if MW_up_t > MW_down_t:
            return (MW_up - MW_down) * 1 / atr55
        else:
            return (MW_down - MW_up) / atr55

        

    def is_slip(self):

        if self.cur_name in self.flip_list:
            return -1
        else:
            return 1
        
       
if __name__ == '__main__':
    for c in ['eurusd','gbpusd','usdchf','audusd','usdcad','usdjpy']:

        t = TradePlan(c,'60')
        print "%f %s" % (t.get_currency_effort() * t.is_slip(),c)
    
    
