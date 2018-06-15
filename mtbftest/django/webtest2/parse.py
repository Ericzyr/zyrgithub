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
    def __init__(self,phoneData):
        self.phoneData = phoneData
        from django.conf import settings
        settings.configure(DEBUG=True, TEMPLATE_DEBUG=True,TEMPLATE_DIRS=(os.path.join(os.path.dirname(__file__), "htmlTemplate"),))

        self.t = get_template("hell.html")

    def writeToFile(self, path):
        html = self.t.render(Context(
            {"testresult": self.phoneData}))


        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        nowtime = str(year) + str(month) + str(day) + "_" + str(hour) + str(minute)
        htmlPath = os.path.join(path , nowtime + ".html")

        with open(htmlPath, 'w') as fp:
            fp.write(html)



        os.system("xdg-open " + htmlPath)



def phoneDataList(args):
    return args


po = HtmlReport(phoneDataList("hello world"))


po.writeToFile("apptest")


