#!/home/tops/bin/python

import os, sys
import logging
import log
import process
import configuration
import magickpy


class ConvertWrapper:
    def __init__(self, config = configuration.Configuration()):
        self.cmd = config.convertbin

    def set_parm(self,**args):
        print args
        
    def convert_copy(self,f,t):
        cp_cmd  = "cp -avf %s %s" % (f, t)
        p = process.Process(cp_cmd)
        p.runInConsole()
        return
    
    
        
        
if __name__ == '__main__':
    c = ConvertWrapper()
    c.set_parm(method='hello',k='v')
    


    
