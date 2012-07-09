#!/home/tops/bin/python
import os, sys, re, string
import time
from glob import glob
import configuration
from currencychart import CurrencyChart
from currencystatus import CurrencyStatus
from ft_utils import *


class Ticket:
    def __init__(self,cur_name,cur_tf,config = configuration.Configuration()):
        self.cur_name           = cur_name.upper()
        self.cur_tf             = cur_tf
        self.ticket_path        = '%s/ticket' % config.forexbase
        
        pass

    def OrderSend(self,**kargs):
        pass

    def OrderMod(self,**kargs):
        pass

    def current(self):
        pass 

    def parser(self):
        ticket_in = '/home/yuting/project/yuting/turbo-daytrader/mql/in/ticket.ordersend'
        
        with open(ticket_in,'r') as f:
            lines  = f.xreadlines()
            for line in lines:
                items = line.strip().split(';')
            f.seek(0)
            f.close()

        if len(items) == 4 or len(items) == 12:
            return items

        print "Error: ticker items number wrong!"
        return []

        
    def new(self):
        pass

if __name__ == '__main__':
    t = Ticket('eurusd','1440')
    print t.parser()
    
