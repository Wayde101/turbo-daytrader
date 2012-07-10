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
        self.CS                      = CurrencyStatus(self.cur_name,cur_tf)
        self.CC                      = CurrencyChart(self.cur_name,cur_tf)
        self.ticket_in          = '%s/ticket.in' %  self.CC.fullpath

        pass


    def OrderSend(self,**kargs):
        self.flip       = kargs['kargs']

    def has_pending_ticket(self):
        print self.ticket_in
        ret = True if os.path.isfile(self.ticket_in) else False
        return ret

    def auto_cc_plan(self):
        status = self.CS.status
        ticket = Ticket(self.cur_name,self.cur_tf)
        if not self.CS.has_cc():
            return
        cmd      = 1 if status['CC']['ZPOINT'] == 'MW_down' else 0
        entry    = float(status['CC']['CC1P'])
        stoploss = float(status['CC']['CC1P']) + 0.0300
        takeprofit= status['CC']['OBJPROP_PRICE1']

        ticket.new(ordertype = 'ordersend', orderbody = {'cmd':cmd,'vol':0.01,'price':entry,'stoploss':stoploss,'takeprofit':takeprofit})
        return

        
if __name__ == '__main__':
    #t = TradePlan('usdcad','10080')
    t = TradePlan('gbpusd','43200')
    t.auto_cc_plan()
    
    
    
