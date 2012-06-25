#! /usr/bin/env python

import subprocess
import time
import signal
import re
import os
import logging
import log

class Process:
    GlobalTimeout = 0
    intervalSecond = 1

    def __init__(self, cmd):
        self.cmd = cmd
        self.logger = logging.getLogger()

    #Note: 
    #  if output of cmd is large or unlimited, please do not use this method.
    #  please use runInConsole and redirect cmd output into file
    def run(self, timeout = GlobalTimeout):
        self.logger.debug(self.cmd)
        p = subprocess.Popen(self.cmd, shell=True, close_fds=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        if timeout > 0:
            self.wait(p, timeout)
        stdout,stderr = p.communicate()
        return (p.returncode, stdout, stderr)

    def runInConsole(self, timeout = GlobalTimeout):
        self.logger.debug(self.cmd)
        p = subprocess.Popen(self.cmd, shell=True)
        if timeout > 0:
            self.wait(p, timeout)
        p.wait()
        return p.returncode

    def runWithoutPipe(self, timeout = GlobalTimeout):
        self.logger.debug(self.cmd)
        tmpOutFile = '.process_run_out'
        tmpErrFile = '.process_run_err'
        self.cmd = self.cmd + ' >' + tmpOutFile +  ' 2>' + tmpErrFile
        retcode = self.runInConsole(timeout)

        stdout = stderr = ''
        if os.path.exists(tmpOutFile):
            stdout = file(tmpOutFile).read()
        if os.path.exists(tmpErrFile):
            stderr = file(tmpErrFile).read()
        return retcode, stdout, stderr

    def wait(self, p, timeout):
        while timeout > 0 and p.poll() == None:
            time.sleep(self.intervalSecond)
            timeout = timeout - self.intervalSecond
        if p.poll() == None and timeout <= 0:
            os.kill(p.pid, signal.SIGKILL)
            self.logger.error("Timeout: kill process [%s]" % self.cmd)

if __name__ ==  "__main__":
    p = Process("ping 10.249.88.45")
    #out, err, code = 
    retcode, stdout, stderr = p.runWithoutPipe(2)
    print 'retcode = ', retcode
    print "out: ", stdout
    print 'err: ', stderr
#    print "out: %s" %(out)
