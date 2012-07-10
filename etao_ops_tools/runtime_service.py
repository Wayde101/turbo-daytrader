#! /usr/bin/env python

import os, sys
import time
import logging
import log
import error

from ha2_configuration import Ha2Configuration
from service_checker import ServiceChecker
from rpc_caller import RpcCallerWrapper
from configuration import Configuration
from nuwa_console_wrapper import NuwaConsoleWrapper
from ha2_tool import Ha2Tool


class RuntimeService:
    intervalSecond = 10

    def __init__(self, pgRoot,configPath,  configuration = Configuration(), serviceName = ''):
        self.configPath = configPath
        self.ha2Configuration =Ha2Configuration(configPath)

        self.configuration = configuration
        self.ha2ToolPath = configuration.ha2ToolPath
        self.ha2Tool = Ha2Tool(pgRoot,configPath,self.ha2ToolPath)
        self.serviceName = serviceName
        self.serviceStatus = None

        self.logger = logging.getLogger()

        #old serving index version:
        self.indexVersionMap = dict()

        #service checker
        self.serviceChecker = ServiceChecker(pgRoot,configPath, configuration)

        #for rollback
        self.restarted = False


    #rollback to last correct version.
    #if not known last correct version, will return False
    def rollback(self, configVersion, clusterIndexVersionMap):
        self.logger.info(']]]]]:rollback config path: [%s]' % self.configPath)
        self.logger.info(']]]]]:rollback index  path: [%s]' % self.configPath)
        return True

    def deployConfiguration(self):
        self.logger.info('deploy configuration for: [%s]' % self.configPath)
        timeout = self.configuration.deployConfigurationTimeout

        if not self.ha2Tool.deployConfiguration(self.serviceName,timeout):
            self.logger.error('deploy configuration error: [%s]' % self.serviceName)
            return False
        return True

    def checkStartCorrect(self):
        if not self.serviceChecker.checkService(self.serviceName):
            return False
        return True

        
     #check service is ready for serving, all partition load success
    def isServiceServing(self):
        serviceStatus = self.getServiceInternalStatus()
        if serviceStatus != 'loaddone':
            return False
        return True

    #stop service
    def stopService(self):
        self.logger.info('stop service: [%s]' % self.configPath)
        timeout = self.configuration.stopServiceTimeout
        if not self.ha2Tool.stopService(self.serviceName,timeout):
            return False

        self.restarted = False
        self.waitForServiceUnload()

        #remove nuwa path for this service

        serviceNuwaRootPath = self.ha2Configuration.getServiceNuwaRootAddress()
        self.logger.info('remove nuwa dir for [%s]' % serviceNuwaRootPath)
        nuwaConsole = NuwaConsoleWrapper(self.configuration.nuwaConsoleBin)
        timeout = self.configuration.commandTimeout
        nuwaConsole.removeIfExists(serviceNuwaRootPath, timeout)
        return True

    def _startServiceByTool(self, timeout):
        return self.ha2Tool.startService(self.serviceName, timeout)

    def startService(self):
        self.logger.info('start service: [%s]' % self.configPath)

        timeout = self.configuration.serviceStartTimeout
        self.serviceName = self._startServiceByTool(timeout)
        if self.serviceName == None:
            self.logger.error('start service failed: [%s]' % self.configPath)
            return error.ERROR_HA2_TOOL_START_SERVICE
        self.logger.debug('start by tool success, service name: [%s]' % self.serviceName)

        timeout = self.configuration.loadPartitionTimeout + self.configuration.serviceWaitingTimeout
        if not self.waitForLoadPartition(timeout):
            return error.ERROR_LOAD_PARTITION_FAILED

        if not self.checkStartCorrect():
            return error.ERROR_LOAD_PARTITION_FAILED

        self.restarted = True
        return error.NO_ERROR

    def buildIncrIndex(self, incr_data):
        self.logger.info('build Inrease data: ', incr_data)

        if not isServiceServing():
            return error.ERROR_CHECK_START_FAILED

        return self.ha2Tool.buildIndex(self.serviceName, timeout)

    def waitForRunningStatus(self, timeout):
        self.logger.info('waiting for running...')
        startTime = time.time()   
        statusStr = self.getServiceStatus()
        while statusStr == None or statusStr == 'Waiting':
            currTime = time.time()
            if startTime + timeout < currTime:
                self.logger.error("wait for service running timeout")
                return False
            time.sleep(self.intervalSecond)
            statusStr = self.getServiceStatus()

        if statusStr == 'Failed':
            self.logger.error("start service failed")
            return False

        self.logger.debug('service is running...')
        return True

    def waitForServiceUnload(self):
        self.logger.info('wait for service unload')
        serviceStatus = self.getServiceInternalStatus()
        while serviceStatus != None:
            time.sleep(5)
            serviceStatus = self.getServiceInternalStatus()

    def waitForLoadPartition(self, timeout):
        self.logger.info('waiting for load partition...')
        startTime = time.time()
        while not self.isServiceServing():
            currTime = time.time()
            if startTime + timeout < currTime:
                self.logger.error("service load index timeout")
                return False
            time.sleep(self.intervalSecond)
        self.logger.debug('service load partition success...')
        return True

    #get service status from  fuxi master
    def getServiceStatus(self):
        timeout = self.configuration.commandTimeout
        rpcCallerWrapper = RpcCallerWrapper(self.ha2Configuration)
        return rpcCallerWrapper.getServiceStatusByFullName(self.serviceName, timeout)

    #get status from server admin
    def getServiceInternalStatus(self):
        timeout = self.configuration.commandTimeout
        return self.ha2Tool.getClusterStatus(self.serviceName,self.configuration, timeout)

def printUsage():
    print >> sys.stderr, sys.argv[0], ' sts config-path'
    print >> sys.stderr, sys.argv[0], ' sps config-path'
    print >> sys.stderr, sys.argv[0], ' rollback config-path'
    print >> sys.stderr, sys.argv[0], ' dp config-path'

def startService(runtimeService):
    if runtimeService.startService() != error.NO_ERROR:
        print 'start service failed'
        sys.exit(1)
    print 'start service successfully'

    status = runtimeService.getServiceStatus()
    if status == None:
        print 'get service status error'
        sys.exit(1)
    print 'get service status successfully'


def stopService(runtimeService):
    if not runtimeService.stopService():
        print 'stop service failed'
        sys.exit(1)
    print 'sttop service successfully'

if __name__ == '__main__':
    if len(sys.argv) < 3:
        printUsage()
        sys.exit(1)
    
    command = sys.argv[1]
    configPath = sys.argv[2]
    runtimeService = RuntimeService(configPath, Configuration(), '1231')
    
    if command == 'sts':
        startService(runtimeService)
        sys.exit(0)
    elif command == 'sps':
        stopService(runtimeService)
        sys.exit(0)
    elif command =='rollback':
        rollbackService(runtimeService)

    print runtimeService.getServiceInternalStatus()

    clusterName = 'daogou_dianping'
    if runtimeService.isServiceServing():
        print clusterName + ' is serving'
    else:
        print clusterName + ' is not serving'

