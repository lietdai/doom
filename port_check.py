#!/usr/bin/env python
# encoding: utf-8
# mail: root@1137.me

import json
import datetime
import sys
import base64
import subprocess
from time import sleep
from libnmap.process import NmapProcess
from libnmap.reportjson import ReportDecoder, ReportEncoder
from libnmap.parser import NmapParser, NmapParserException
from libnmap.plugins.backendpluginFactory import BackendPluginFactory

from util.secmail import *


global_flag = "port_vul"

#global_dbcoon = 'mysql+mysqldb://root:123456@127.0.0.1:3306/wscan'


global_words = {
    #心脏滴血check
    "openssl" : {
        "script" : "exp/PoC.py -p %(port)s %(address)s",
        "port" : [443,587,465,995,8443],
        "service" : ["https","smtp","pop","imap","https-alt"],
        "banner": "None"
    },
    "structs" : {
        "script" : "exp/new_check_struts2.py %(address)s %(port)s",
        "port": [80,81,8080,8000,8443,9090],
        "service":["http","http-alt","http-proxy","unknown","xmpp"],
        "banner": "None"
    },
    "svn":{
        "script" : "exp/svn.py %(address)s %(port)s",
        "port" : [80,443],
        "service":["http","http-alt","https","http-proxy","unknown","xmpp"],
        "banner" : "None"
    },
    "iis":{
        "script" : "exp/iis.py %(address)s %(port)s",
        "port" : [80,81,8080,8000,8443,9090],
        "service": ["None"],
        "banner": "iis"
    },
    "classloader":{
        "script" : "exp/classloader.py %(address)s %(port)s",
        "port" : [80,443],
        "service":["http","http-alt","http-proxy","unknown","xmpp"],
        "banner" : "None"
    },
    "hydra":{
        "script" : "exp/hydra.py %(address)s %(service)s %(port)s",
        "port" : [21,22,3306],
        "service": ["ssh","mysql","ftp","smtp"],
        "banner": "None"
    },
    "backup":{
        "script" : "exp/backup_check.php -t %(address)s -p %(port)s",
        "port": [80,81,8080,8000,8443,9090],
        "service":["http","http-alt","http-proxy","unknown","xmpp"],
        "banner" : "None"
    },
    "shockbash":{
        "script": "exp/shellshock.py %(address)s %(port)s",
        "port": [80,81,8080,8000,8443,9090],
        "service":["http","http-alt","http-proxy","unknown","xmpp"],
        "banner" : "None"
    },
    "fastcgi":{
        "script": "exp/fast_cgi.py %(address)s",
        "port" : [9000],
        "service": ["None"],
        "banner" : "None"
    },
    "es20153337":{
        "script": "exp/es20153337.py %(address)s /etc/passwd",
        "port" : [9200],
        "service": ["None"],
        "banner" : "None"
    },
    "WeakBanner":{
        "script": "exp/jboss.py %(address)s %(port)s",
        "port": [80,81,8080,8000,8443,9090],
        "service":["http","http-alt","http-proxy","unknown","xmpp"],
        "banner":"JBoss"
    },
    "banner":{
        "script": "exp/banner.py %(address)s %(port)s",
        "port": [80,81,443,88,8080,8081,8000,8443,9090],
        "service":["http","https","https-alt","http-alt","http-proxy","unknown","xmpp"],
        "banner":"None"
    },
    "rsync":{
        "script": "exp/rsync.py %(address)s %(port)s",
        "port": [873],
        "service":["rsync"],
        "banner":"extrainfo"        
    },
    "test" : {
        "script" : "exp/test.py",
        "port" : [3306],
        "service" : ["mysql"],
        "banner": "None"
    }
}

def subExec2(command, timeout):
    start = datetime.datetime.now()
    process = subprocess.Popen(command, bufsize=10000, stdout=subprocess.PIPE, close_fds=True)
    while process.poll() is None:
        time.sleep(0.1)
        now = datetime.datetime.now()
        if (now - start).seconds> timeout:
            try:
                process.terminate()
            except Exception,e:
                return None
            return None
    out = process.communicate()[0]
    if process.stdin:
        process.stdin.close()
    if process.stdout:
        process.stdout.close()
    if process.stderr:
        process.stderr.close()
    try:
        process.kill()
    except OSError:
        pass
    return out

def subExec(cmdline):
    cmd_proc = subprocess.Popen(cmdline,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)

    process_output = cmd_proc.stdout.readlines()        
    return '\n'.join(process_output)


def portDispath(address, service, taskId = "None"):
    if blockCheck(target):
        return None
    #print service
    #data example
    #address 127.0.0.1
    #service {u'protocol': u'tcp', u'service': u'mysql', u'state': u'open', u'id': u'tcp.3306', u'reason': u'syn-ack', u'banner': u'product: MySQL version: 5.5.44-0+deb8u1', u'port': u'3306'}
    # taskId =.= 
    
    for exp in global_words:
        if int(service['port']) in global_words[exp]['port'] or  service['service'] in global_words[exp]['service'] or   global_words[exp]['banner'].lower() in service['banner']:            
            cmdLine =  global_words[exp]['script'] % {'port':service['port'],'service':service['service'],'address':address}
            print exp
            res = subExec(cmdLine)
            if res.find("wakaka") > -1:
                data =   "Vuln: \n"+"address: "+address+"\nport: "+service['port']+"\nservice:  "+service['service']+"\n"+"cmd: "+cmdLine+"\nresult: \n"+res
                subject = "[PORT_SEC]"+"["+taskId.upper()+"]"+exp+" vuln "+address+":"+service['port']
                print subject,data,taskId

                secmail().send("root@1137.me", subject, data)
    return False

def blockCheck(target):
    fileObject = open('block.list', 'rb')
    for line in fileObject:
        if line.strip() == target:
            return True
    return False
        


if __name__ == "__main__":
    address  = sys.argv[1].strip()
    service = json.loads( base64.b64decode(sys.argv[2].strip()))
    if len(sys.argv) == 4:
        taskId = sys.argv[3].strip()
    elif len(sys.argv) == 5:
        taskId = sys.argv[4].strip()
    else:
        taskId = "None"
    portDispath(address,service,taskId)
    sys.exit(0)

        
