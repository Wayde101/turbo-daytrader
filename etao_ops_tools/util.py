#! /usr/bin/env python 

import sys, socket
import process


def getaddrbyhost(host):
    result = socket.getaddrinfo(host, None)
    return result[0][4][0]


def get_map_value(map, key, default_value):
    if key in map:
        return map[key]
    return default_value

def getConfigPath(serviceName):
    return serviceName + '_config'

def getPartitionNum(docCount, maxDocPerPartition):
    return ((docCount + maxDocPerPartition - 1) // maxDocPerPartition)


def joinPanguPath(panguRoot, path):
    if panguRoot[-1] == '/':
        return panguRoot + path
    return panguRoot + '/' + path


if __name__ == '__main__':
    print getaddrbyhost('localcluster')
    print getaddrbyhost('10.249.88.45')
    print getaddrbyhost('myhost')
    
