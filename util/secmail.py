#!/usr/bin/env python  
#-*- coding: utf-8 -*-
# date : 2015-05-12
# author : 1137

import os, sys, string, socket
import smtplib
import email.utils
from email.mime.text import MIMEText


class secmail(object):

    username = "your email address"
    password = "your email password"
    smtpServer = "smtp.exmail.qq.com"
    port = 465

    def __init__(self,s= smtpServer, u = username, p = password):
        self.server = smtplib.SMTP(s)

    def send(self, to, subject, body):
        msg = MIMEText(body)
        msg.set_unixfrom('author')
        msg['to'] = email.utils.formataddr(('Master',to))
        msg['from'] = email.utils.formataddr(('Robot',self.username))
        msg['subject'] = subject
        try:
            #self.server.set_debuglevel(True)
            self.server.ehlo()
            
            if self.server.has_extn('STARTTLS'):
                self.server.starttls()
                self.server.ehlo()
                self.server.login(self.username, self.password)
                self.server.sendmail(self.username,
                                [to],
                                msg.as_string())

        finally:
            self.server.quit()


if __name__ == "__main__":
    secmail().send("root@1137.me","subject","aaaaaaaaaaa")
