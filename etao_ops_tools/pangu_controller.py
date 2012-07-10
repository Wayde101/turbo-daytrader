#! /usr/bin/env python

import os, sys, re
import time
import logging 
import log
import process

class PanguController:
    def __init__(self, cycle = 1):
        self.cycle = cycle
        self.startFile = 'pangu_restarter.py'
        self.logger = logging.getLogger()

    def __restartPangu(self, gatewayIp, maxUnnormalCSNum, timeout = 0):
        if self.cycle <= 0 or ((int(time.time() // 86400) % self.cycle) != 0):
            self.logger.info('need not restart pangu')
            return True

        currPath = os.path.dirname(__file__)
        srcFile = os.path.join(currPath, self.startFile)
        destFile = '/tmp/' + self.startFile
        if not self.scpFileTo(srcFile, gatewayIp, destFile):
            self.logger.error('copy file to [%s] error' % gatewayIp)
            return False
        restartCmd = 'python %s %d' % (destFile, maxUnnormalCSNum)
        if not self.remoteRun(gatewayIp, restartCmd, timeout):
            self.logger.error('restart pangu error')
            return False
        return True

    def restartPangu(self, gatewayIp, maxUnnormalCSNum, timeout = 0):
        for i in range(0, 3):
            if self.__restartPangu(gatewayIp, maxUnnormalCSNum, timeout):
                return True
        return False

    def scpFileTo(self, srcFile, destHost, destFile):
        cmd = 'scp %s %s:%s' % (srcFile, destHost, destFile)
        p = process.Process(cmd)
        retcode, stdout, stderr = p.run()
        if retcode != 0:
            self.logger.error('%s error: %s' %(cmd, stderr))
            return False
        return True

    def remoteRun(self, destHost, cmd, timeout = 0):
        cmd = 'ssh %s %s' % (destHost, cmd)
        p = process.Process(cmd)
        retcode, stdout, stderr = p.runWithoutPipe(timeout)
        if retcode != 0:
            self.logger.error('%s error: %s' % (cmd, stdout + stderr))
            return False
        self.logger.debug('run %s success: [%s]' %(cmd, stdout))
        return True

    def setStartPanguFile(self, fileName):
        self.startFile = fileName

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print >> sys.stderr, 'Usage: %s host-ip max-unnormal-chunserver [cycle]'
        sys.exit(1)

    destHost = sys.argv[1]
    maxUnnormalCSNum = int(sys.argv[2])

    if len(sys.argv) >= 4:
        cycle = int(sys.argv[3])
    else:
        cycle = 1

    panguController = PanguController(cycle)
    #panguController.setStartPanguFile('test_python.py')
    if not panguController.restartPangu(destHost, maxUnnormalCSNum):
        print >> sys.stderr, 'restart pangu failed'
        sys.exit(1)
    print 'restart pangu success'
    
        
        
