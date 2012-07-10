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
        self.ticket_path        = '%s/%s_%s' % (config.ticketbase,\
                                                self.cur_name, \
                                                self.cur_tf)
        self.ticket_slippage           = 3
        self.ordercomment       = 'order_from_%s_%s' % (self.cur_name,self.cur_tf)
        self.status             = CurrencyStatus(self.cur_name,self.cur_tf).status



    def parse_ordersend(self):
        ticket_file = '%s/ticket.in' % self.ticket_path
        
        if self.has_pending_ticket() == False:
            return False

        with open(ticket_file,'r') as f:
            lines  = f.xreadlines()
            for line in lines:
                items = line.strip().split(';')
            f.seek(0)
            f.close()

        if len(items) == 12:
            self.ticket_type        = items[0]
            self.ticket_cmd         = items[2]
            self.ticket_vol         = items[3]
            self.ticket_price       = items[4]
            self.ticket_slippage    = items[5]
            self.ticket_stoploss    = items[6]
            self.ticket_takeprofit  = items[7]
            self.ticket_comment     = items[8]
            self.ticket_magic       = items[9]
            self.ticket_expiration  = items[10]
        else:
            print "Error: ticker items number wrong!"
            return False
            
        return True

    def has_pending_ticket(self):
        ticket_file = '%s/ticket.in' % self.ticket_path
        return os.path.exists(ticket_file)

    def remove(self):
        ticket_file = '%s/ticket.in' % self.ticket_path
        os.unlink(ticket_file)
        
    def new(self,**kargs):
        ticket_file = '%s/ticket.in' % self.ticket_path
        order_cmd_str = ''

        if kargs['ordertype']  == 'ordersend':
            if not (kargs['orderbody'].has_key('cmd') and \
                    kargs['orderbody'].has_key('vol') and \
                    kargs['orderbody'].has_key('price') and \
                    kargs['orderbody'].has_key('stoploss') and \
                    kargs['orderbody'].has_key('takeprofit')):
                print 'cmd/vol/price/stoploss/takeprofit key(s) missing'
                return order_cmd_str
                
            order_cmd_str='OBJNAME=OrderSend;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s' % \
                (self.cur_name,\
                kargs['orderbody']['cmd'],\
                kargs['orderbody']['vol'],\
                kargs['orderbody']['price'],\
                self.ticket_slippage if not kargs['orderbody'].has_key('ticket_slippage') else \
                kargs['orderbody']['ticket_slippage'],\
                kargs['orderbody']['stoploss'],\
                kargs['orderbody']['takeprofit'],\
                self.ordercomment if not kargs['orderbody'].has_key('comment') else \
                kargs['orderbody']['comment'],\
                self.cur_tf if not kargs['orderbody'].has_key('magic') else \
                kargs['orderbody']['magic'],\
                '0' if not kargs['orderbody'].has_key('expiration') else  \
                kargs['orderbody']['expiration'],\
                'RED' if kargs['orderbody']['cmd'] == 0 else 'GREEN')
            
        elif kargs['ordertype'] == 'ordermod':
            if not (kargs['orderbody'].has_key('ticket') and \
                    kargs['orderbody'].has_key('stoploss') and \
                    kargs['orderbody'].has_key('takeprofit')):
                print 'ticket/stoploss/takeprofit key(s) missing'
                return order_cmd_str
            
            order_cmd_str = 'OBJNAME=OrderModify;%s;%s;%s' % \
                (kargs['orderbody']['ticket'],\
                kargs['orderbody']['stoploss'], \
                kargs['orderbody']['takeprofit'])
            
        else:
            print "Unknown order type"

        with open(ticket_file,'w') as f:
            f.write(order_cmd_str)
            f.close()
        return order_cmd_str

if __name__ == '__main__':
    t = Ticket('eurusd','60')
    print sys.argv
    if sys.argv[1] == '1':
        print t.new(ordertype = 'ordersend',orderbody = {'cmd':1,'vol':0.1,'price':1.2676,'stoploss':1.2706,'takeprofit':1.2482})
        print t.has_pending_ticket()
        print t.parse_ordersend()
    if sys.argv[1] == '2':
        print t.status
        

    
    #print t.remove()
    #print t.new(ordertype = 'ordermod',orderbody = {'ticket':1,'stoploss':1.4888,'takeprofit':1.9999})
    
