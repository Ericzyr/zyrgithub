#!/usr/bin/env python3
# -*-coding:utf-8-*-
from __future__ import division

from imp import reload

from django.template import Context
from datetime import datetime
import django
import json
import os
import re
import sys

try:
    from django.template.loader import get_template
except Exception as e:
    # print("It appears that Django is not installed. Please install Django")
    # print('from the included file Django-1.2.3.tar.gz. The version of ')
    # print("Django available with your Linux distribution, if you are ")
    # print("using one, may not be suitable. Unzip and untar the zip ")
    # print("into any directory, cd into the folder, and, as ")
    # print("administrator, run:")
    # print("python setup.py install")
    sys.exit()

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

reload(sys)

sys.setdefaultencoding("utf-8")


class HtmlReport():
    def __init__(self , phoneData , dataFC , dataTB , dataANR , dataReset , totalExeTime , totalError , dataPass ,
                 dataExce , passRate , mtbfVal):
        self.phoneData = phoneData
        self.dataFC = dataFC
        self.dataTB = dataTB
        self.dataANR = dataANR
        self.dataPass = dataPass
        self.dataExce = dataExce
        self.dataReset = dataReset
        self.totalExeTime = totalExeTime
        self.totalError = totalError
        self.mtbfVal = mtbfVal
        self.passRate = passRate
        from django.conf import settings
        settings.configure(DEBUG=True , TEMPLATE_DEBUG=True,TEMPLATE_DIRS=(os.path.join(os.path.dirname(__file__), "htmlTemplate"),))
        # djangoVersion = django.get_version()[0:3]
        # if djangoVersion == '1.7':
        #     django.setup()
        self.t = get_template("child.html")

    def writeToFile(self, path):
        html = self.t.render(Context(
            {"testresult": self.phoneData , "totalANR": self.dataANR , "totalTombstone": self.dataTB ,
             "totalFC": self.dataFC , "totalReset": self.dataReset , "totalExeTime": self.totalExeTime ,
             "totalError": self.totalError , "totalcasePass": self.dataPass , "totalcaseExce": self.dataExce ,
             "passRate": self.passRate , "mtbfValue": self.mtbfVal}))
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        nowtime = str(year) + str(month) + str(day) + "_" + str(hour) + str(minute)
        htmlPath = os.path.join(path , nowtime + ".html")
        with open(htmlPath , 'w') as fp:
            fp.write(html)


def phoneDataList(args):
    pass

def dataFC(args):
    pass

po = HtmlReport(phoneDataList,0,0,0,0,0,0, 0,0,0,0)

po.writeToFile("apptest_TV")
