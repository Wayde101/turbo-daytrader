#! /usr/bin/env python

import sys, os, re
import time
import subprocess
import logging
import log

import process

class AbenchWrapper:
    def __init__(self, executable = None):
        if executable != None:
            self.executable = executable
        else:
            self.executable = 'abench'
        self.logger = logging.getLogger()

    def startAbench(self, queryPath, qrsAddr, threadNum, timeLen):
        cmd = '%s -p %d -s %d --apsara %s Search %s' % \
             (self.executable, threadNum, timeLen, qrsAddr, queryPath)
        p = process.Process(cmd)
        retcode, stdout, stderr = p.runWithoutPipe()
        
    def startMultiAbench(self, queryPaths, qrsAddrs, threadNum, timeLen):
        #if len(queryPaths) != len(qrsAddrs):
        #    raise ValueError, 'qrsAddrs must equal to queryPaths'
        if len(queryPaths) == 0:
            return True
        if len(qrsAddrs) == 0:
            raise ValueError, 'param list qrsAddrs is empty'

        cmdPattern = '%s -p %d -s %d --apsara %s Search %s'
        processArray = list()
        qrsIndex = 0
        for queryPath in queryPaths:
            qrsAddr = qrsAddrs[qrsIndex]
            cmd = cmdPattern % (self.executable, threadNum, timeLen, \
                                qrsAddr, queryPath)
            cmd = cmd + (' >abench.out.%d 2>abench.out.%d' % (qrsIndex, qrsIndex))
            self.logger.debug(cmd)
            p = subprocess.Popen(cmd, shell=True)
            processArray.append(p)
            qrsIndex = (qrsIndex + 1) % len(qrsAddrs)
        
        remainProcessArray = []
        success = True
        while len(processArray) > 0:
            for p in processArray:
                if p.poll() == None:
                    remainProcessArray.append(p)
                else:
                    retcode = p.wait()
                    if retcode != 0:
                        success = False
            processArray = remainProcessArray
            remainProcessArray = []
        return success

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print 'Usage: %s query_path_list qrs_list thread-num time-len' % sys.argv[0]
        sys.exit(1)

    queryPathList = re.split(',', sys.argv[1].strip())
    qrsList = re.split(',', sys.argv[2].strip())
    threadNum = int(sys.argv[3])
    timeLen = int(sys.argv[4])

    abenchWrapper = AbenchWrapper()
    success = abenchWrapper.startMultiAbench(queryPathList, qrsList, threadNum, timeLen)
    if not success:
        print 'abench failed'
        sys.exit(1)
    print 'abench success'
    
        
