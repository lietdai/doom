#!/usr/bin/env python  
#-*- coding: utf-8 -*-
# date : 2015-05-12
# author : 1137

import pymongo
import time


class MongoTool(object):
    """mongo op"""
    host = "127.0.0.1"
    port = 27017

    def __init__(self, host = host , port=port):
        try:
            self.conn = pymongo.Connection(host,port)
        except Exception :
            print 'connect to %s:%s fail' %(host, port)
            exit(0)

    def __del__(self):
        self.conn.close()


        
if __name__ == "__main__":
    #Mongo.checkDb()
    table  = MongoTool().conn.request.log
    table.insert({"a":1,"b":2})
    print table.find_one({"a":1})
