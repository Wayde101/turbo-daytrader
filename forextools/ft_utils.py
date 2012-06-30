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

