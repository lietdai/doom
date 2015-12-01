DOOM_SEC
=======
DOOM_SEC是在thorn上实现的分布式任务分发的ip端口漏洞扫描器



nmap扫描端口分发，可port，service，banner多种命中,检测插件可水平拓展

依赖https://github.com/ring04h/thorns ,向ring0致敬


##关于任务调度

 跳转到https://github.com/ring04h/thorns 


##关于port分发命中
你能从nmap中拿到的结果是port,service,banner。所以你需要根据三个参数来命中你的扫描插件

目前已经添加的检测模块是`心脏滴血`、`structs远程代码执行`、`svn泄露`、`IIS TTP.sys检测`、`struts classloader漏洞检测`、`常见端口弱口令`、`破壳漏洞`、`备份代码扫描`、
`jboss及zabbix扫描`、`http服务banner的收集`、`es部分漏洞`等
```python
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
```

##如何添加一个插件

在exp目录下添加你的exp，检测到存在漏洞后输出`wakaka～`即可，如这个弱口令扫描的

```
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
    
    
```

命中输出wakaka即可


##如何使用

* 参考thorn
* 你需要修改以下两个文件的smtp信息的配置为你的
  * util/phpmail.php
 * util/secmail.py
* 部分插件依赖mongo，mysql，redis，请安装他们

##最后

**Enjoy It**



