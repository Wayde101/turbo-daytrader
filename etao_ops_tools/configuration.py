#! /usr/bin/env python


class Configuration:
    #NOTE: must be same order with configuration in aggregator
    clusterConfigPaths = [
        '/apsarapangu/disk5/daogou/crontab/pe_code/index_switcher/ay33_kuafu2',
        '/apsarapangu/disk5/daogou/crontab/pe_code/index_switcher/ay33_kuafu2'
        ]

    noCopy = ''

    nuwaConsoleBin = '/apsara/deploy/nuwa_console'
    ha2ToolPath = '/apsarapangu/disk5/daogou/crontab/pe_code/index_switcher/console'

    # config for ha2 service
    services = {
        "daogou_combo" : ['daogou_zixun', 'daogou_luntan', 'daogou_wenda'],
        "daogou_auction" : ['daogou_auction'] 
        }



    #check service start correct
    serviceCheckQueries = ['nokia']

    # timeout config

    idxCopyRetryTimes         = 3
    serviceStartTimeout       = 120
    indexBuildTimeout         = 40000
    serviceWaitingTimeout     = 600
    loadPartitionTimeout      = 1200
    changeIndexVersionTimeout = 120
    stopServiceTimeout        = 120
    deployConfigurationTimeout = 1200
    commandTimeout            = 20
    indexCopyTimeout          = 7200
    searchOneQueryTimeout     = 10

    #aggregator config
    aggregatorIps = ['10.249.103.34' ]

    aggregatorScriptFile = '/home/admin/aggregator/switch.py'
    switchAggregatorTimeout = 60

    doneFile = "hdfs://10.249.69.101:9000/user/daogou/indexbuilder/data/current/.builddone"
    copyingFile = "hdfs://10.249.69.101:9000/user/daogou/indexbuilder/data/current/.copying"
    
    #copy data from hadoop config
    comboMap = {'daogou_luntan' : 'bbs',
                'daogou_wenda'    : 'question',
                # 'daogou_dianping' : ['dump_comment_record'],
                'daogou_zixun'    : 'news',
                'daogou_auction'  : 'auction'
             }
    hadoopDumpRoot = '/user/daogou/indexbuilder/data/current/'
    panguDataRoot = '/home/admin/daogou/' 

    # incr data conf section
    checkInterval  = 60
    hadoopIncrRoot = '/user/daogou/incrDump/data/current/'
    panguIncrRoot  = '/home/admin/daogou/incr_data/'
    
    eagleLogFile = '/usr/local/eagleye/log/sec.log'
    copyDataForOneClusterTimeout = 3600

    # abench warm up config
    abenchBin = '/apsara/deploy/abench-apasara0.8'
    queryLogMap = {'daogou_luntan'   : 'luntan_query.txt',
                   'daogou_wenda'    : 'wenda_query.txt',
                   # 'daogou_dianping' : 'dianping_query.txt',
                   'daogou_zixun'    : 'zixun_query.txt',
                   'daogou_auction'  : 'auction_query.txt'
                   }
    abenchThreadNum = 20
    abenchTimeLen   = 900
    RpcCallerExe    = '/apsara/deploy/rpc_caller'
    Ha2UserName     = 'admin'

    def __init__(self):
        pass
