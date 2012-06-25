#! /usr/bin/env python

import sys, os, re
import time
import logging
import log

from configuration import Configuration
from ha2_tool import Ha2Tool
from nuwa_console_wrapper import NuwaConsoleWrapper

class ServiceChecker:
    def __init__(self, pgRoot,configPath, config = Configuration()):
        self.configPath  = configPath
        self.pgAddr      = pgRoot
        self.configuration = config
        self.ha2Tool = Ha2Tool(pgRoot,configPath,config.ha2ToolPath)
        self.logger = logging.getLogger()

    def searchQueryForCluster(self, serviceName,clusterName, query, timeout = 0):
        self.logger.info('search query [%s] for cluster [%s]' % (query, clusterName))

        for i in range(3):
            result = self.ha2Tool.searchQuery(serviceName, clusterName, query, timeout)
            if result == None:
                self.removeNuwaAddress()
                time.sleep(30)
                continue                     
            pattern = re.compile('<hits\s+numhits="(\d+)"\s+totalhits="(\d+)">')
            match = re.search(pattern, result)
            if match == None:            
                self.logger.error('not found hit pattern: [%s]' % result)
                time.sleep(30)
                continue
            numHits = int(match.group(1))
            totalHits = int(match.group(2))
            self.logger.debug('numHits = %d totalHits = %d' % (numHits, totalHits))
            if numHits != 0 and totalHits != 0:
                return True
        return False

        
    def removeNuwaAddress(self):
        serviceNuwaRootPath = self.ha2Configuration.getServiceNuwaRootAddress()
        nuwaConsole = NuwaConsoleWrapper(self.configuration.nuwaConsoleBin)
        timeout = self.configuration.commandTimeout
        if not nuwaConsole.removeIfExists(serviceNuwaRootPath, timeout):
            self.logger.error('remove nuwa address fail: [%s]' % serviceNuwaRootPath)
            return False
        return True

    def checkService(self,serviceName):
        timeout = self.configuration.searchOneQueryTimeout
        clusters = self.configuration.services[serviceName]
        for cluster in clusters:
            for query in self.configuration.serviceCheckQueries:
                if not self.searchQueryForCluster(serviceName,cluster, query, timeout):
                    self.logger.error('check cluster [%s] error', cluster)
                    return False
        return True
        
def printUsage():
    print >> sys.stderr, sys.argv[0], " config-path"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        printUsage()
        sys.exit(1)
    pgRoot='pangu://10.249.49.2:10240/home/admin/daogou/'
    sn='daogou_auction'
    serviceChecker = ServiceChecker(pgRoot,sys.argv[1])
    if serviceChecker.checkService(sn):
        print 'check service successfully'
    else:
        print 'check service failed'
        sys.exit(1)
