#! /usr/bin/env python

import os, sys
import pexpect
import logging
import log
import error

import process
import configuration

class AggregatorWrapper:
    def __init__(self, config = configuration.Configuration()):
        self.hostIps = config.aggregatorIps
        self.scriptFile = config.aggregatorScriptFile
        self.logger = logging.getLogger()
    
    def _switchHostWithoutUser(self, ip, idx, timeout):
        cmd = 'ssh ' + ip + ' python ' + self.scriptFile + ' ' + str(idx)
        self.logger.debug(cmd)
        p = process.Process(cmd)
        retcode, stdout, stderr = p.run(timeout)
        self.logger.debug('ret:[%d], stdout, [%s], stderr:[%s]' % \
                          (retcode, stdout, stderr))
        if retcode != 0 or stdout.strip().endswith('failed!'):
            self.logger.debug('switch aggregator failed: [%s]' % ip)
            return False
        
        return True
    
    def _switchHostWithUser(self, ip, idx, userName, passwd, timeout):
        cmd = 'ssh ' + ip + ' python ' + self.scriptFile + ' ' + str(idx)
        self.logger.debug(cmd)
        child = pexpect.spawn(cmd)
        while True:
            expectList = ['.*word:', 'yes\|no\)', '.*ok!', '.*failed!', '.+',
                          pexpect.EOF, pexpect.TIMEOUT]
            idx = child.expect(expectList, timeout=timeout)
            if idx == 0:
                child.sendline(passwd)
            elif idx == 1:
                child.seldline('yes')
            elif idx == 2:
                return True
            elif idx > 4:
                self.logger.error('timeout or no response')
                return False
            else:
                self.logger.debug('switch aggregator failed')
                return False
        return True

    def _switchHost(self, hostIp, idx, userName, passwd, timeout):
        if userName == None:
            return self._switchHostWithoutUser(hostIp, idx, timeout)
        else:
            return self._switchHostWithUser(hostIp, idx, userName, passwd, timeout)
    
    def stop(self, idx, userName = None, passwd = None, timeout = 60):
        #if idx > 1 or idx < 0:
        #    self.logger.error('illegal idx: [%d]' % idx)
        #    return False

        internalIdx = 1 - idx
        for hostIp in self.hostIps:
            if not self._switchHost(hostIp, internalIdx, userName, passwd, timeout):
                return False
        return True

    def recover(self, userName = None, passwd = None, timeout = 60):
        for hostIp in self.hostIps:
            if not self._switchHost(hostIp, 9, userName, passwd, timeout):
                return False
        return True

def printUsage():
    print >> sys.stderr, sys.argv[0], ' stop <num>'
    print >> sys.stderr, sys.argv[0], ' stopWithUser <num> userName passwd'
    print >> sys.stderr, sys.argv[0], ' recover'

def assertArgsNum(argc):
    if len(sys.argv) < argc:
        printUsage()
        sys.exit(1)
        
if __name__ == '__main__':
    assertArgsNum(2)

    aggregator = AggregatorWrapper()
    command = sys.argv[1]
    
    if command == 'stop':
        assertArgsNum(3)
        if not aggregator.stop(int(sys.argv[2])):
            print >> sys.stderr, 'switch aggregator failed'
            sys.exit(1)
        print 'switch aggregator success'
    elif command == 'stopWithUser':
        assertArgsNum(5)
        if not aggregator.stop(int(sys.argv[2]), sys.argv[3], sys.argv[4]):
            print >> sys.stderr, 'switch with user aggregator failed'
            sys.exit(1)
        print 'switch with user aggregator success'
    elif command == 'recover':
        if not aggregator.recover():
            print >> sys.stderr, 'recover aggregator failed'
            sys.exit(1)
            print 'recover aggregator success'
    else:
        print >> sys.stderr, 'unsupport operation'
        sys.exit(1)
