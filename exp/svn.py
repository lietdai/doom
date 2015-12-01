#!/usr/bin/python
#coding:utf-8
#author:root@1137.me

import urllib2
import time
import Queue
import threading
import httplib
import json
import sys


class RedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        pass
    def http_error_302(self, req, fp, code, msg, headers):
        pass



def check_svn(url):
    html = ''
    try:
        urlsvn = url+"/.svn/entries"
        opener = urllib2.build_opener(RedirectHandler)
        response = opener.open(urlsvn,timeout=4)
        try:
            html = response.read()
            html = json.loads(html)
            pass
        except:
            if (html and "svn:" in html) or ("dir" in html and "DoCTYPE" not in html and "DOCTYPE" not in html and "<script" not in html and "Active connections" not in html and html !="([]);" and len(html.strip())>0):
                print urlsvn+"~wakaka"
                print html
    except Exception, e:
        pass

def check_git(url):
    html = ''
    try:
        urlgit = url+"/.git/config"
        opener = urllib2.build_opener(RedirectHandler)
        response = opener.open(urlgit,timeout=4)
        try:
            html = response.read()
            html = json.loads(html)
            pass
        except:
            if (html and "core" in html) or ("origin" in html and "DoCTYPE" not in html and "DOCTYPE" not in html and "<script" not in html and "Active connections" not in html and html !="([]);" and len(html.strip())>0):
                print urlgit+"~wakaka"
                print html
    except Exception, e:
        pass
    

if __name__ == "__main__":
    if len(sys.argv) == 3:        
        target = sys.argv[1]
        port = sys.argv[2]
        if port == 443:
            url = "https://"+target
        else:
            url = "http://"+target+":"+port
        check_svn(url)
        check_git(url)
        #test()
