#! /usr/bin/env python

NO_ERROR = 0

ERROR_DEPLOY_CONFIGURATION        = 1001
ERROR_START_BUILD                 = 1002
ERROR_STOP_BUILD                  = 1003

ERROR_COPY_INDEX                  = 2001

#increase releated
ERROR_COPY_INCR_DATA              = 5001
ERROR_CHECK_INCR_DATA             = 5002
ERROR_BUILD_INCR_INDEX            = 5003
ERROR_STOP_BUILD_JOB              = 5004
ERROR_GET_INCR_STATUS             = 5005
ERROR_INCR_MOVE_PG                = 5006
ERROR_INCR_MOVE_HDP               = 5007
ERROR_NO_INCR_DATA                = 5008

ERROR_STOP_SERVICE                = 2002
ERROR_HA2_TOOL_START_SERVICE      = 2003
ERROR_SERVICE_WAITING_TIMEOUT     = 2004
ERROR_LOAD_PARTITION_FAILED       = 2005
ERROR_QUERY_FAILED                = 2006


ERROR_CHECK_START_FAILED         = 2008
ERROR_CHANGE_ACTIVE_INDEX_VERSION = 2009

ERROR_SWITCH_PROXY_ERROR          =  2010
ERROR_RESTART_PANGU_FAILED        = 2011
ERROR_SWITCH_INDEX                =  2012

ERROR_COMMAND_TIMEOUT            = 3001
ERROR_COMMAND_FAILED              = 3002
ERROR_OPERATION_TIMEOUT           = 3003

ERROR_OTHER_ERROR                 = 4001


def getErrorMessage(errorNo):
    if errorNo == ERROR_DEPLOY_CONFIGURATION:
        return "deploy configuration error"
    elif errorNo == ERROR_START_BUILD:
        return "start build error"
    elif errorNo == ERROR_SWITCH_INDEX:
        return "switch index error"
    elif errorNo == ERROR_STOP_BUILD:
        return "stop build job error"
    elif errorNo == ERROR_COPY_INDEX:
        return "copy index error"
    elif errorNo == ERROR_HA2_TOOL_START_SERVICE:
        return 'start service by ha2 tool error'
    elif errorNo == ERROR_SERVICE_WAITING_TIMEOUT:
        return 'service waiting timeout'
    elif errorNo == ERROR_STOP_SERVICE:
        return "stop service error"
    elif errorNo == ERROR_QUERY_FAILED:
        return "query failed"
    elif errorNo == ERROR_SWITCH_PROXY_ERROR:
        return "switch aggregator failed"
    elif errorNo == ERROR_CHECK_START_FAILED:
        return "check start service correctly failed"
    elif errorNo == ERROR_COMMAND_FAILED:
        return "apsara cmd failed"
    elif errorNo == ERROR_OPERATION_TIMEOUT:
        return "operation timeout"
    elif errorNo == ERROR_RESTART_PANGU_FAILED:
        return "restart pangu failed"
    else:
        return "unkown error"
