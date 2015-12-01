#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, DateTime, LargeBinary, Text, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from libnmap.plugins.backendplugin import NmapBackendPlugin
from libnmap.reportjson import ReportEncoder, ReportDecoder

import json
from datetime import datetime
import binascii

Base = declarative_base()

class NmapSqlPlugin(NmapBackendPlugin):
    """
        This class handle the persistence of NmapRepport object in SQL backend
        Implementation is made using sqlalchemy(0.8.1)
        usage :

        #get a nmapReport object
        from libnmap.parser import NmapParser
        from libnmap.reportjson import ReportDecoder, ReportEncoder
        import json
        nmap_report_obj = NmapParser.parse_fromfile(
               '/home/vagrant/python-nmap-lib/libnmap/test/files/1_hosts.xml')

         #get a backend with in memory sqlite
         from libnmap.plugins.backendpluginFactory import BackendPluginFactory
         mybackend_mem = BackendPluginFactory.create(plugin_name='sql',
                                                     url='sqlite://',
                                                     echo=True)

         mybackend_mysql = BackendPluginFactory.create(plugin_name='sql',
                            url='mysql+mysqldb://scott:tiger@localhost/foo',
                            echo=True)
         mybackend = BackendPluginFactory.create(plugin_name='sql',
                                        url='sqlite:////tmp/reportdb.sql',
                                        echo=True)
         #lets save!!
         nmap_report_obj.save(mybackend)
         mybackend.getall()
         mybackend.get(1)
    """
    class Reports(Base):
        """
            Embeded class for ORM map NmapReport to a
            simple three column table
        """
        __tablename__ = 'result_report'

        id = Column('id', Integer, primary_key=True)
        target = Column('target', String(64))
        inserted = Column('inserted', DateTime(), default='now')
        vul_type = Column('vul_type', String(32))
        vul_detail = Column('vul_detail', Text)



        def __init__(self):
            self.inserted = datetime.now()
            pass


        def decode(self):
            pass
            

    def __init__(self, **kwargs):
        """
            constructor receive a **kwargs as the **kwargs in the sqlalchemy
            create_engine() method (see sqlalchemy docs)
            You must add to this **kwargs an 'url' key with the url to your
            database
            This constructor will :
            - create all the necessary obj to discuss with the DB
            - create all the mapping(ORM)

            todo : suport the : sqlalchemy.engine_from_config

            :param **kwargs:
            :raises: ValueError if no url is given,
                    all exception sqlalchemy can throw
            ie sqlite in memory url='sqlite://' echo=True
            ie sqlite file on hd url='sqlite:////tmp/reportdb.sql' echo=True
            ie mysql url='mysql+mysqldb://scott:tiger@localhost/foo'
        """
        NmapBackendPlugin.__init__(self)
        self.engine = None
        self.url = None
        self.Session = sessionmaker()

        if 'url' not in kwargs:
            raise ValueError
        self.url = kwargs['url']
        del kwargs['url']
        try:
            self.engine = create_engine(self.url, **kwargs)
            Base.metadata.create_all(bind=self.engine, checkfirst=True)
            self.Session.configure(bind=self.engine)
        except:
            raise


    def add(self, target, vul_type, vul_detail):        
        sess = self.Session()
        row = NmapSqlPlugin.Reports()
        row.target = target
        row.vul_type = vul_type
        row.vul_detail = vul_detail
        sess.add(row)
        sess.commit()
        reportid = row.id
        sess.close()
        return reportid if reportid else None
