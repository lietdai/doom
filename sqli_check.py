#!/usr/bin/env python
# encoding: utf-8
# mail: root@1137.me

import json
import sys
import base64
import os
from time import sleep
from libnmap.process import NmapProcess
from libnmap.reportjson import ReportDecoder, ReportEncoder
from libnmap.parser import NmapParser, NmapParserException
from libnmap.plugins.backendpluginFactory import BackendPluginFactory




from  util.req  import Req




global_sqlmap = "/usr/bin/sqlmap"

global_options = " --batch  --smart "

global_notify = "--alert='python "+sys.path[0]+"/"+sys.argv[0]+" notify "

global_flag = "sqli_vul"

global_dbcoon = 'mysql+mysqldb://root:123456@127.0.0.1:3306/wscan'



def sqliCheck(request, platform = None):
    reqObj = Req(request)

     #method filiter
    if reqObj.method != "GET" and reqObj.method !=   "POST":
         return None

     #后缀删除
    ext = getExtByUri(reqObj.uri)
    if ext in ["gif","js","jpg","css","png","ico"]:        
        return None
     #无参数 filter
    if reqObj.method != "POST" and len(reqObj.url.split('=')) == 1:
        return None

    my_services_backend = BackendPluginFactory.create(plugin_name='backend_permission', url=global_dbcoon, echo=False, encoding='utf-8', pool_timeout=3600)
 

    reqFile = req2file(reqObj.hash,request)
    notify = global_notify + reqFile + "\'"
    cmd = global_sqlmap+ " -r "+reqFile + global_options + notify
    print cmd
    outPut = os.popen(cmd)
    return     outPut.read()


def getExtByUri(uri):
    ext =  uri.split('?')[0].split('.')
    if len(ext) > 1 :
        return ext[-1]
    return None


def req2file(code, request):
    fileName =  "/tmp/"+code+".tmp"
    fh = file(fileName, "wb")
    fh.write(request)
    fh.close()
    return fileName





if __name__ == "__main__":
    if len(sys.argv) == 2:
        argv1 = base64.b64decode(sys.argv[1])    
        print sqliCheck(argv1)
    elif len(sys.argv) == 3:        
        fh = open(sys.argv[2],'rb')
        try:
            data = fh.read( )
        finally:
            fh.close( )
        my_services_backend = BackendPluginFactory.create(plugin_name='backend_permission', url=global_dbcoon, echo=False, encoding='utf-8', pool_timeout=3600)
        reqObj = Req(data)
        target = reqObj.host
        vul_type = global_flag
        vul_detail ="SQLi Vul:\n"+data
        my_services_backend.add(target,vul_type,vul_detail)
        #print "VUL" if permissionCheck(reqStr) else "SAFE"

        sys.exit(0)
    else:
        print ("usage: %s base64(request)" % sys.argv[0])
        sys.exit(-1)

