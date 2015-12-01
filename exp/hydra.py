#!/usr/bin/python
#coding:utf-8
#author:root@1137.me

import sys
import subprocess
import time

globalUserFile = "exp/hydra/user.txt"
globalPassFile = "exp/hydra/pass.txt"
globalTimeout = 60
def hydraCheck(target,port,service):
    cmdLine = 'hydra  -L %s -P %s -s %s -e ns %s %s' %(globalUserFile, globalPassFile, port, target, service )
    print cmdLine
    proc = subprocess.Popen(cmdLine,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
    deadline = time.time() + globalTimeout
    while time.time() < deadline and proc.poll() == None:
        time.sleep(globalTimeout)
    if proc.poll() == None:
        proc.terminate()
    output,stderr = proc.communicate()
    print output
    #output = proc.stdout.readlines()    
    if "password" in output:
        print "~wakaka"
    return output
    
    

if __name__ == "__main__":
    if len(sys.argv) == 4:        
        target = sys.argv[1]
        service = sys.argv[2]
        port = sys.argv[3]
        hydraCheck(target, port, service)
        
