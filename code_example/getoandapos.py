#!/usr/bin/env python


import urllib, urllib2, re


def oanda_fetch():
    url      = "http://fxtrade.oanda.com/analysis/open-position-ratios"
    #dst_file = "/home/yuting/turbo-daytrader/code_example/mytest.html"
    dst_file = "/home/yuting/src/phpmyadmin/myhtml/mytest.html"

    fh = open(dst_file,'w')
    
    f  = urllib2.urlopen(url)
    data = f.read()

    pos_begin = data.find('<h3>Long-Short Ratios</h3>')
    pos_end   = data.find('<div class="orderbook-ratio-graph" id="orderbook-open-position">')
    
    if pos_begin  == -1 or pos_end == -1:
        return False

    ls_part = data[pos_begin:pos_end]

    print >>fh , ls_part
    #print "pos_begin [%s], pos_end [%s]" % (pos_begin,pos_end)
    
    #print data



if __name__ == '__main__':

    oanda_fetch()

    
    
