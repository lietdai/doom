#!/usr/bin/python
#coding:utf-8
#author:root@1137.me

from bs4 import BeautifulSoup
import requests
import threading
import Queue
import time
import sys
import json
sys.path.append('./util/')  
from mongotool import MongoTool

def btdk(url):
    try:
        req = requests.get(url, timeout = 5)
        html = req.text
        headers = req.headers
    except:                                
        print "http request error!"
        sys.exit(0)
        #html = '<html><title>%s</title><meta name="keywords" content="" /><meta name="description" content="" /></html>'%url
    soup = BeautifulSoup(html.lower())
    t = soup.title.text.encode('utf8','ignore').decode("utf8")
    #t = soup.title.text
    try:
        k = soup.find(attrs={"name":"keywords"})['content'].encode('utf8','ignore')
    except:
        k = ""
    try:
        d = soup.find(attrs={"name":"description"})['content'].encode('utf8','ignore')
    except:
        d = ""
    
    return headers,t,d,k


if __name__ == '__main__':
    #url = "http://210.14.138.1"
    if len(sys.argv) == 3:        
        target = sys.argv[1]
        port = sys.argv[2]
        if port == 443:
            protocal = "https"
        else:
            protocal = "http"
        url = protocal+"://"+target+":"+str(port)
        (h,t,d,k) = btdk(url)
        row = {
            "ip" : target,
            "port" : port,
            "headers" : dict(h),
            "title" : t,
            "keywords" : d,
            "desc" : k
        }
        table  = MongoTool().conn.request.banner
        print table.insert(row)
    #print table.find_one({"a":2})
