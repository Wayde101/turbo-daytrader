#!/home/tops/bin/python

import os, sys ,re,string
import time
from glob import glob
import configuration
from currencychart import CurrencyChart
from currencystatus import CurrencyStatus
from ft_utils import *


class CcWatcher:
    def __init__(self, config = configuration.Configuration()):
        self.timeframe = ['60','240','1440','10080','43200']
        self.currency  = ['eurusd','gbpusd','usdchf','audusd','usdcad','usdjpy']
    
    
    
    
    
