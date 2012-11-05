#!/usr/bin/env python
import os, sys
import re
import process
import logging
import log

class HadoopTool:
    def __init__(self, toolPath):
        self.toolPath = toolPath
        self.hadoopbin = self.toolPath + '/hadoop'
        self.logger = logging.getLogger()
    
    def hadoopInvoke(self, cmd, timeout = 0):
        p = process.Process(cmd)
        code, data, error = p.run(timeout)
        return code, data, error

    def listDirectory(self, path, timeout = 0):
        cmd = self.hadoopbin + ' dfs -ls ' + path
        code, data, error = self.hadoopInvoke(cmd, timeout)
        if code != 0:
            return None
        data = data.strip('\n\r\t ')
        if len(data) == 0:
            return list()

        lines = data.split('\n')
        del lines[0]
        ret = []
        for line in lines:
            items = re.split('\s+', line.strip(' \t'))
            if len (items) != 8: 
                return None
            ret.append(items[7])
        return ret

    def isPathExists(self, path, timeout = 0):
        cmd = self.hadoopbin + ' dfs -test -e ' + path
        code, data, error = self.hadoopInvoke(cmd, timeout)
        if code == 255:
            raise RuntimeError, "hadoop fs -test -e error"
        if code != 0:
            return False
        return True

    def touch(self, h2pready, timeout = 0):
        cmd = self.hadoopbin + ' dfs -touchz ' + h2pready
        p = process.Process(cmd)
        code, data, error = p.run(timeout)
        if code == 255:
            raise RuntimeError, "dfs -touch z error"
        if code != 0:
            return False
        else:
            return True

    def remove(self, fn, timeout = 0):
        cmd = self.hadoopbin + ' dfs -rm ' + fn
        p = process.Process(cmd)
        code, data, error = p.run(timeout)
        if code == 255:
            raise RuntimeError, "remove error"
        if code != 0:
            return False
        else:
            return True

    def move(self, src, dest, timeout = 0):
        cmd = self.hadoopbin + ' dfs -mv %s %s' % (src, dest)
        p = process.Process(cmd)
        code, data, error = p.run(timeout)
        if code == 255:
            raise RuntimeError, "dfs -mv  error"
        if code != 0:
            return False
        return True

    def mkdir(self, dirname, timeout = 0):
        cmd = self.hadoopbin + ' dfs -mkdir %s' % (dirname)
        p = process.Process(cmd)
        code, data, error = p.run(timeout)
        if code == 255:
            raise RuntimeError, "dfs -mkdir  error"
        if code != 0:
            return False
        return True

            

if __name__ == '__main__':
   toolPath = './hadoop_client/bin'
   hTool = HadoopTool(toolPath)
   def userage():
       print 'hadoopTool -ls /hadooppath/ \n'

   if len(sys.argv) < 2:
       userage()
       sys.exit(1)
   if sys.argv[1] == '-ls':
       hadooppath = sys.argv[2]
       ret = hTool.listDirectory(hadooppath)
       if ret != None:
           print ret
           sys.exit(0)
       else:
           print 'hadoop ls error!!!'
           sys.exit(1)
   else:
       print 'not support command'
