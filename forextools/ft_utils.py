#!/home/tops/bin/python

import os, sys ,re,string


def read_time(rg):
    time_seg = -1
    p=re.compile('^\s*(\d+)\s*(\w*)')
    if p.match(rg):
        c,d = (int(p.search(rg).groups(1)[0]),p.search(rg).groups(1)[1])
        if re.search('^m(in(ute)?s?)?$',d):
            time_seg = c * 60
        elif re.search('^h((ou)?rs?)?$',d):
            time_seg = c * 3600
        elif re.search('^d(ays?)?$',d):
            time_seg = c * 86400
        else:
            print "unkown time unit"
            time_seg = -1
    else:
        print "wrong format"
    return time_seg


def read_timeframe(rg):

    if rg == '5m' or rg == '5M' or rg == '5':
        return 5
    elif rg == '15m' or rg == '15M' or rg == '15':
        return 15
    elif rg == '1h' or rg == '1H' or rg == '60':
        return 60
    elif rg == '4h' or rg == '4H' or rg == '240':
        return 240
    elif rg == '1d' or rg == '1D' or rg == '1440':
        return 1440
    elif rg == '1w' or rg == '1W' or rg == '10080':
        return 10080
    elif rg == '1M' or rg == '1M' or rg == 'MN' or rg == 'mn' or rg == '43200':
        return 43200

    
