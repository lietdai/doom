#!/usr/bin/env python  
#-*- coding: utf-8 -*-
# date : 2015-04-30
# author : 1137

import hashlib
import time
from mongotool import MongoTool

class Req:
    """分解 request 请求"""
    def __init__(self,req):
        self.method = None
        self.url = None
        self.host = None
        self.headers = {}                
        self.protocol = None
        self.data = ""
        self.hash = ""
        self.selfCheck()                
        line = req.strip().split('\n')        
        line0 = line[0].split()        
        self.method = line0[0]
        if line0[1].startswith("http"):            
            self.uri = line0[1][self.findStr(line0[1],"/",3):]
        else:
            self.uri = line0[1]
        self.protocol = line0[2]
        
        dataCheck = 0
        for x in line[1:]:
            if dataCheck == 1:
                self.data += x.strip()
                continue
            if not x.strip():
                dataCheck = 1
            header =  x.split(':',1)        
            if header[0].strip() == 'Host':
                self.host = header[1].strip()
                tmp  = self.host.split(":",1)                            
                if len(tmp) > 1:
                    self.port = int(tmp[1])
                else:
                    self.port = 80
                self.url = "http://"+self.host+self.uri
                continue
            if len(header) == 2 and header[0] != 'Proxy-Connection':                                
                self.headers[header[0]] =  header[1].strip()
        self.hash = hashlib.md5(self.uri.strip()).hexdigest()
    def findStr(self, string, subStr, findCnt):
        listStr = string.split(subStr,findCnt)
        if len(listStr) <= findCnt:
            return -1
        return len(string)-len(listStr[-1])-len(subStr)

    def selfCheck(self):
        pass

    def log(self):
        """all request log into mongodb"""
        #reqHash = hashlib.md5(self.url.split('?')[0].strip()).hexdigest()
        #reqHash = hashlib.md5(self.url.strip()).hexdigest()
        table = MongoTool().conn.request.log
        res = table.find_one({"hash":self.hash})
        if res == None:
            row = self.__dict__
            row['hash'] = self.hash
            row['time'] = int(time.time())
            row['check'] = 0
            row['data'] = row['data'].decode("unicode_escape")
            table.insert(row)
            print "\033[1;31m%s\033[0m" % "Log Request "+row['url']
    
