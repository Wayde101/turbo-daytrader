#! /usr/bin/env python

import os, sys
import util
import process
import logging
import log

from ha2_configuration import Ha2Configuration

class RpcCallerWrapper:
    def __init__(self, ha2Configuration, env = None):
        self.ha2Configuration = ha2Configuration
        self.excutable = self.ha2Configuration.getRpcCallExe()        
        self.nuwaAddress = ha2Configuration.getNuwaServiceIp()
        self.nuwaIp = ''

        #may throw exception 
        pos = self.nuwaAddress.find(':');
        if pos == -1:
            self.nuwaIp = util.getaddrbyhost(self.nuwaAddress)
        else:
            self.nuwaIp = util.getaddrbyhost(self.nuwaAddress[0:pos]) + \
                          self.nuwaAddress[pos:]
        self.logger = logging.getLogger()

    def invoke(self, cmd, timeout = 0):
        p = process.Process(cmd)
        code, data, error = p.run(timeout)
        return code, data, error
        
    def _getServiceStatusByFullName(self, serviceName, timeout = 0):
        cmd = self.excutable + ' --Server=' + self.ha2Configuration.getFuxiServer() + \
              ' --Method=GetWorkItemStatus --Parameter=' + serviceName
        retcode, stdout, stderr = self.invoke(cmd, timeout)
        self.logger.debug('status: ' + stdout + stderr)
        if retcode != 0:
            self.logger.error('get service status error: ' + serviceName)
            return None
        pos = stdout.find('Return=')
        if pos == -1:
            return None

        status = stdout[pos + 7:].strip()
        if len(status.strip()) == 0:
            self.logger.error('get service status failed: [%s]' % serviceName)
            return None
        return status

    def _getJobStatusByFullName(self,jobName,timeout=0):
        cmd = self.excutable + ' --Server=' + self.ha2Configuration.getFuxiServer() + \
              ' --Method=GetWorkItemStatus --Parameter=' + jobName
        retcode, stdout, stderr = self.invoke(cmd, timeout)
        self.logger.debug('status: ' + stdout + stderr)
        if retcode != 0:
            self.logger.error('get service status error: ' + jobName)
            return None
        pos = stdout.find('Return=')
        if pos == -1:
            return None

        status = stdout[pos + 7:].strip()
        if len(status.strip()) == 0:
            self.logger.error('get service status failed: [%s]' % serviceName)
            return None
        return status

    def getServiceStatusByFullName(self, serviceName, timeout = 0):
        for i in range(0, 3):
            status = self._getServiceStatusByFullName(serviceName, timeout)
            if status != None:
                return status
        return None

    def getServiceStatusByName(self, serviceName, timeout = 0):
        fullServiceName = "nuwa://" + self.nuwaIp + '/' +  \
            serviceName + '/ServiceMaster'
        return getServiceStatusByFullName(fullServiceName)

    def getServiceStatusById(self, serviceId, timeout = 0):
        fullServiceName = "nuwa://" + self.nuwaIp + '/' +  \
            self.ha2Configuration.getUserName() + '/' + str(serviceId) + '/ServiceMaster'
        return self.getServiceStatusByFullName(fullServiceName)


if __name__ == '__main__':
    ha2Configuration = Ha2Configuration('../tools_test/ay16_kuafu1/daogou_combo_config')
    rpcCaller = RpcCallerWrapper(ha2Configuration)
    print rpcCaller.getServiceStatusByFullName('353')
