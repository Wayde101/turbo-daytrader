#! /usr/bin/env python
import os, sys
import time
import logging
import log 
import process
import re

from pangu_wrapper import PanguWrapper

class Hdfs2Pangu:
    def __init__(self,yishanConfDir=None):
        path = os.path.dirname(__file__)
        if len(path) == 0:
            path = '.'
        self.yishan2 = path + '/yishan_hadoop.py'
        self.logger = logging.getLogger()
        if(yishanConfDir == None):
            self.confdir = path
        else:
            self.confdir = yishanConfDir

    def copyData(self, src, dest, timeout = 0):
        time_format = '%Y-%m-%d-%s'
        out_time = time.strftime(time_format,time.localtime())
        ysoutfile = 'hdfs2pangu%s.log' % out_time 
        cmd = self.yishan2 + ' -s %s -d %s -c %s > %s 2>&1' % (src, dest, self.confdir ,ysoutfile)
        retcode = self.copyInvoke(cmd, timeout)
        if retcode != 0:
           self.logger.error('yishan copy data faild from hadoop')
           return False
        if self.checkHdfs2panguSuccess(ysoutfile):
            return True
        return False

    def getDestNuwa(self):
        yishanConfFile = os.path.join(os.path.dirname(__file__), './yishan2.conf')
        for line in open(yishanConfFile):
            line = line.strip()
            if line.startswith('destnuwa'):
                pos = line.find('=')
                return line[pos+1:].strip()
        return None

    def checkHdfs2panguSuccess(self, outfile):
        regExpr = re.compile('transfer\s+complete\s*:\s*true\s$', re.IGNORECASE)
        lastLine = ''
        for line in open(outfile):
            lastLine = line
        if re.search(regExpr, line):
            return True
        return False
    
    def copyInvoke(self, cmd, timeout = 0):
        p = process.Process(cmd)
        rst = p.runInConsole(timeout)
        return rst

if __name__ == '__main__':
    def useage():
        print 'hdfs2pangu.py -s /hadoop_path/ -d /pangu_path/'

    if len (sys.argv) < 5:
        useage()
        sys.exit(1)
    if sys.argv[1] == '-s':
        src = sys.argv[2]
    else:
        useage()
        sys.exit(1)
    if sys.argv[3] == '-d':
        dest = sys.argv[4]
    else:
        useage()
        sys.exit(1) 
    h2p = Hdfs2Pangu()
    if h2p.copyData(src, dest):
        print 'runing yisha2 is ok!!!'
    else:
        print 'runing yisha2 is filed !!!'
