#!/usr/bin/env python
#coding:utf-8
#author: l137

import socket
import random
import sys

def check_iis(ip,port):
    ipAddr = ip
    hexAllFfff = "18446744073709551615"
    req = "GET / HTTP/1.1\r\nHost: stuff\r\nRange: bytes=0-" + hexAllFfff + "\r\n\r\n"
    timeout=1
    socket.setdefaulttimeout(timeout)
    #测试是否有leak
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ipAddr, int(port)))
        client_socket.send(req)
        goodResp = client_socket.recv(1024)
        if "Requested Range Not Satisfiable" in goodResp and "IIS" in goodResp:
            print "[%s] Looks VULN" % ipAddr + "~wakaka"
    except:
        pass

    
if __name__ == "__main__":
    if len(sys.argv) == 3:        
        target = sys.argv[1]
        port = sys.argv[2]
        check_iis(target,port)
