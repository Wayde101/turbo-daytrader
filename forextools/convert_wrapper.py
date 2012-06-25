#! /usr/bin/env python

import os, sys
import logging
import log
import process
import configuration


class ConvertWrapper:
    def __init__(self, config = configuration.Configuration()):
        self.cmd = config.convertbin

    def set_parm(self,**args):
        print args
        
    def convert_copy(self,f,t):
        
        
if __name__ == '__main__':
    c = ConvertWrapper()
    c.set_parm(method='hello',k='v')
    


    
