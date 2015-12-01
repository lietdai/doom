#!/usr/bin/env python
#coding:utf-8
#author: l137

import sys
import time
import urllib2



def checkJbossRce(ip,port):

    url = "http://"+ip+":"+str(port)+"/invoker/JMXInvokerServlet"
    req = urllib2.Request(url)
    try:
        info = urllib2.urlopen(req,timeout=5).read()
        if "jboss" in info:
            print "jboss wakaka~~"        
    except Exception,e:
        pass

def checkZabbix(ip, port):
    url = "http://"+ip+":"+str(port)+"/zabbix/"
    req = urllib2.Request(url)
    try:
        info = urllib2.urlopen(req,timeout=5).read()
        if "Zabbix" in info:
            print "Zabbix wakaka~~"        
    except Exception,e:
        pass



if __name__ == "__main__":
    if len(sys.argv) == 3:        
        target = sys.argv[1]
        port = sys.argv[2]
        checkJbossRce(target, port)
        checkZabbix(target, port)
