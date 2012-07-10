#!/bin/env python

import error
import os, sys, re, time
import logging
from incr_controller import IncrController

from optparse import OptionParser

if __name__ == '__main__':
    controller = IncrController()

    def RunAllOpt(option,opt_str,value,parser):
        while True:
            controller.run()
            time.sleep(300)

    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage=usage)

    parser.add_option("--run-all"     ,action="callback",callback=RunAllOpt)
    (options, args) = parser.parse_args()
