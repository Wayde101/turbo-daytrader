#! /usr/bin/env python

import sys
from configuration import Configuration
from controller import Controller

def printUsage():
    print >> sys.stderr, "Usage: ", sys.argv[0], " [0|1]"

def checkArgs():
    if len(sys.argv) < 2:
        printUsage()
        sys.exit(1)
        
    choice = sys.argv[1]
    if choice not in ['0', '1']:
        printUsage()
        sys.exit(1)


def runUpdate(choice):
    comboMap1 = {
        'daogou_luntan' : ['bbs'],
        'daogou_wenda'    : ['question'],
        # 'daogou_dianping' : ['dump_comment_record'],
        'daogou_zixun'    : ['news'],
        'daogou_auction'  : ['auction']
        }
    
    comboMap2 = {
        'daogou_wenda'    : ['question'],
        # 'daogou_dianping' : ['comment_record'],
        'daogou_auction'  : ['auction']
        }

    comboMapArray = [comboMap1, comboMap2]

    services1 = {
        "daogou_combo" : ['daogou_wenda', 'daogou_zixun', 'daogou_luntan'], 
        "daogou_auction" : ['daogou_auction'] 
        }

    services2 = {
        "daogou_combo" : ['daogou_dianping', 'daogou_wenda'], 
        "daogou_auction" : ['daogou_auction'] 
        }
    servicesArray = [services1, services2]
    
    config = Configuration()
    # config.noCopy = '/apsarapangu/disk5/daogou/crontab/pe_code/index_switcher/ay33_kuafu2'
    config.services = servicesArray[choice]
    config.comboMap = comboMapArray[choice]
    
    controller = Controller(config)
    if not controller.run():
        return False
    return True

if __name__ == '__main__':
    checkArgs()
    choice = int(sys.argv[1])
    if not runUpdate(choice):
        sys.exit(1)
    sys.exit(0)
    
    
