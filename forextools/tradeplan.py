#!/home/tops/bin/python

import os, sys ,re,string
import time
from glob import glob
import configuration
from currencychart import CurrencyChart
from currencystatus import CurrencyStatus
from ft_utils import *


class TradePlan:
    def __init__(self,cur_name,cur_tf,config = configuration.Configuration()):
        self.cur_name           = cur_name.upper()
        self.cur_tf             = cur_tf
        CS                      = CurrencyStatus(cur_name,cur_tf)
        CC                      = CurrencyChart(cur_name,cur_tf)
        self.ticket_in          = '%s/ticket.in' %  CC.fullpath

        pass


    def OrderSend(self,**kargs):
        self.flip       = kargs['kargs']

    def has_ticket(self):
        print self.ticket_in
        ret = True if os.path.isfile(self.ticket_in) else False
        return ret


        

        
if __name__ == '__main__':
    t = TradePlan('eurusd','60')
    print t.has_ticket()
    
    
