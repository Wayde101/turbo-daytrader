#! /usr/bin/env python

import sys, re
import logging
import process
import log
import time

class NuwaConsoleWrapper:
    def __init__(self, executable):
        self.executable = executable
        self.logger = logging.getLogger()

    def listDirectory(self, address, timeout = 0):
        cmd = 'nuwa_console --address=%s' % address
        p = process.Process(cmd)
        retcode, stdout, stderr = p.runWithoutPipe(timeout)
        if retcode != 0:
            return None
        errorPattern = 'Error:\s+St9exception|Exception:'
        if re.compile(errorPattern).search(stdout + stderr):
            return None
        retArray = []
        lines = stdout.strip().split('\n')
        for line in lines:
            if not re.compile('^\s+').match(line):
                retArray.append(line)
        return retArray

    def remove(self, address, timeout = 0):
        cmd = 'echo _delete | nuwa_console --address=%s --console --admin' % address
        if not self.runNuwaCmd(cmd, timeout):
            return False
        return True

    def isPathExists(self, address, timeout = 0):
        cmd = 'echo ls | nuwa_console --address=%s --console --admin | head' % address
        if not self.runNuwaCmd(cmd, timeout):
            return False
        return True

    def _removeIfExists(self, address, timeout = 0):
        if not self.isPathExists(address, timeout):
            self.logger.debug('path %s not exists' % address)
            return True
        if not self.remove(address, timeout):
            self.logger.debug('remove nuwa path failed: ' + address)
            return False

    def removeIfExists(self, address, timeout = 0):
        for i in range(0, 3):
            if self._removeIfExists(address, timeout):
                return True
            self.logger.error('remove address [%s] failed' % address)
        return False

    def runNuwaCmd(self, cmd, timeout = 0):
        p = process.Process(cmd)
        retcode, stdout, stderr = p.runWithoutPipe(timeout)
        if retcode != 0:
            return False
       
        errorPattern = 'Error:\s+St9exception|Exception:'
        if re.compile(errorPattern).search(stdout + stderr):
            return False
        return True
        
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print >> sys.stderr, "Usage: ", sys.argv[0], " [exist|delete|die] nuwa_dir"
        sys.exit(1)
    
    excutable = 'nuwa_console'
    nuwaConsole = NuwaConsoleWrapper(excutable)
    command = sys.argv[1]
    nuwaAddress = sys.argv[2]
    if command == 'isexist':
        if nuwaConsole.isPathExists(nuwaAddress):
            print 'dir %s exists' % nuwaAddress
        else:
            print 'dir %s not exists' % nuwaAddress
    elif command == 'delete':
        if nuwaConsole.remove(nuwaAddress):
            print 'remove dir %s success' % nuwaAddress
        else:
            print 'remove dir %s failed' % nuwaAddress
    elif command == 'die':
        if nuwaConsole.removeIfExists(nuwaAddress):
            print 'remove dir %s success' % nuwaAddress
        else:
            print 'remove dir %s failed' % nuwaAddress
    else:
        print 'unsupport command'
        sys.exit(1)
