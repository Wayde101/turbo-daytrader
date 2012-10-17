#!/usr/bin/env python

import os, sys ,re
from configuration import Configuration
from yishan_hadoop import YishanConfig

sys.path.append(Configuration.ha2ToolPath + '/src/')
from include import json

DEF_FUXISERVER = 'sys/fuxi/master/ForChildMaster'
DEF_QRS_PORT   = 'QueryResultServerRole/'

class Ha2Configuration:
    def __init__(self, configPath):
        
        self.configuration=Configuration()
        self.yishanConf  = YishanConfig(configPath + '/../')
        self.nuwaAddr    = self.yishanConf.destnuwa + ':' + self.yishanConf.nuwa_port
        self.configPath  = configPath
        p=re.compile('(.*)_config')
        if p.match(configPath):
            # ugly guess serviceName
            self.serviceName = os.path.split(p.search(configPath).groups(1)[0])[1]
        else:
            print "configPath parse error [%s]" % configPath
            sys.exit(1)

    def getConfigPath(self):
        return self.configPath

    def getRpcCallExe(self):
        return self.configuration.RpcCallerExe
    
    def getFuxiServer(self):
        return "nuwa://" + self.nuwaAddr + '/'+ DEF_FUXISERVER
    
    def getNuwaServiceIp(self):
        return self.nuwaAddr

    def getUserName(self):
        return self.configuration.Ha2UserName

    def getQrsAddress(self):
        QrsPort = '%(Nuwa)s/%(User)s/%(Server)s/%(Port)s' % {
            'Nuwa'    : "nuwa://" + self.nuwaAddr,
            'User'    : self.configuration.Ha2UserName,
            'Server'  : self.serviceName,
            'Port'    : DEF_QRS_PORT }

        return QrsPort

    def getServiceNuwaRootAddress(self):
        return '%(Nuwa)s/%(User)s/%(Server)s/' % {
            'Nuwa'    : "nuwa://" + self.nuwaAddr,
            'User'    : self.configuration.Ha2UserName,
            'Server' : self.serviceName }


    def getServiceClusters(self):
        return self.configuration.services[self.serviceName]

    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print >> sys.stderr, sys.argv[0], ' config-path'
        sys.exit(1)

    configuration = Ha2Configuration(sys.argv[1])
    print configuration.getConfigPath()
    print configuration.getRpcCallExe()
    print configuration.getFuxiServer()
    print configuration.getNuwaServiceIp()
    print configuration.getServiceClusters()
    print configuration.getQrsAddress()
    print configuration.getServiceNuwaRootAddress()
