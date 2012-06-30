#!/home/tops/bin/python

import os, sys
import logging
import log
import process
import configuration

class ConvertWrapper:
    def __init__(self, config = configuration.Configuration()):
        self.convert   = config.convertbin
        self.set_parm()
        
    def set_parm(self,**kargs):
        self.flip      = kargs['flip'] if kargs.has_key('flip') else False
        self.pointsize = kargs['pointsize'] if kargs.has_key('pointsize') else 40
        self.text      = kargs['text'] if kargs.has_key('text') else 'unknown'
        
    def convert_copy(self,f,t):
        flip_opt = text_opt = pointsize_opt = ''

        if f == 'noimgs':
            print "NoImgs to convert ."
            return

        if self.flip:
            flip_opt = '-flip'

        text_opt = '-draw \'text 10,50 "%s"\'' % self.text
        pointsize_opt = '-pointsize %d' % 40
        
        cv_cmd  = "%s %s %s %s %s %s" % (self.convert,
                                   flip_opt,
                                   pointsize_opt,
                                   text_opt,
                                   f,t)
        p = process.Process(cv_cmd)
        p.runInConsole()
        return
        
        
if __name__ == '__main__':
    c = ConvertWrapper()
    c.set_parm(flip=False,text='usdjpy_43200')
    c.convert_copy('/home/yuting/project/yuting/Alpari/experts/files/shots/USDJPY_43200/1338508800.gif','/tmp/jpy.gif')
    
