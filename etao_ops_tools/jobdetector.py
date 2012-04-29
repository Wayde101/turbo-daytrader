#!/usr/bin/env python

import sys, os, time
import re
import logging


class JobDetector:
    def __init__(self):
        self.logger = logging.getLogger()

        # 0 : all jobs got passed. argu with wali.
    def detectJobs(self, jobIds, jobTimeout = 36000, cmdTimeout = 5):
        self.printLog('INFO: detecting logs')
        return 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: ', sys.argv[0], 'jobid1 jobid2 ...'
        sys.exit(1)
        
    jobIds = []
    for i in range(1, len(sys.argv)):
         jobIds.append(int(sys.argv[i]))

    jobDetector = JobDetector()
    ret = jobDetector.detectJobs(jobIds)
    print ret
        
