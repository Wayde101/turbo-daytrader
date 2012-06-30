#! /usr/bin/env python
import os, sys, re, time
import pickle
import logging
import configuration
import util
import error
import simplejson
import re

from pangu_wrapper import PanguWrapper
from ha2_configuration import Ha2Configuration




class indexCleaner:
    def __init__(self,configuration = configuration.Configuration()):
        self.config = configuration
        self.panguRoot = "/home/admin/admin/"
        self.force = "false"
        self.cluster = 'ay25a'
        self.ha2conf = ''
        self.pu_con  = PanguWrapper()

        
    def get_active_number(self, by_scn ):
        
        if not self.ha2conf:
            print >> sys.stderr, 'ha2 config missing'
            exit(1)

        jsonMap = simplejson.loads(self.pu_con.getPanguFileContent(self.ha2conf.getDataActiveFilePath( by_scn )))
        return int(jsonMap["active_version_num"])

    def get_list_removed ( self ):
        
        p=re.compile('generation_([0-9]*)')

        for service in self.config.services:
            for cluster_config_path in self.config.clusterConfigPaths:
                self.ha2conf=Ha2Configuration(cluster_config_path + '/' + service + '_config' )
                for scn in self.ha2conf.getServiceClusters():
                    scn_act_num = self.get_active_number( scn )
                    
                    dist_path='pangu://' + self.ha2conf.getNuwaServiceIp() + self.ha2conf.getDataPathForIndexCopy( scn )
                    for line in self.pu_con.listPanguDirectory(dist_path):
                        if p.match(line):
                            pat_num = p.search(line).groups(1)[0]
                            rmpath  = dist_path + 'generation_' + pat_num
                            if scn_act_num - int(pat_num) > 6:
                                self.pu_con.removeDir( rmpath )

        return(1)
        # return pu_con.listPanguDirectory(,timeout=5);

    def run(self,num):
        rm_items = self.get_list_removed()

def showUsage():
    print >> sys.stderr, sys.argv[0] + ' <keep_number>'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        showUsage()
        sys.exit(1)
        
    cleaner = indexCleaner()
    if sys.argv[1] < 5:
        print "Warning: 5 days at least"
        exit(1)
        
    cleaner.run(sys.argv[1])
            
        
    
