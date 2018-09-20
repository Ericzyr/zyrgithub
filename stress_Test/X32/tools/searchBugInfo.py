#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from django.template import Context
import os
import sys
import django
from datetime import datetime
from jira import JIRA
try:
	from django.template.loader import get_template
except Exception, e:
	print "It appears that Django is not installed. Please install Django"
	print "from the included file Django-1.2.3.tar.gz. The version of "
	print "Django available with your Linux distribution, if you are "
	print "using one, may not be suitable. Unzip and untar the zip "
	print "into any directory, cd into the folder, and, as "
	print "administrator, run:"
	print "python setup.py install"
	sys.exit()

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

reload(sys)
sys.setdefaultencoding('utf-8')
#########################define global variable#####################
BugID = "BugID.text"

######################################################################
class HtmlReport():
	def __init__(self, bugData):
		self.bugData = bugData
		from django.conf import settings
		settings.configure(DEBUG=True, TEMPLATE_DEBUG=True,
 		    TEMPLATE_DIRS=(os.path.join(os.path.dirname(__file__), 'htmlTemplate'),))
		djangoVersion = django.get_version()[0:3]
		if djangoVersion == '1.7':
 			django.setup()
		self.t = get_template("BugChild.html")

	def writeToFile(self, path):
		html = self.t.render(Context({"bugData":self.bugData}))
		now = datetime.now()
		year = now.year
		month = now.month
		day = now.day
		hour = now.hour
		minute = now.minute
		nowtime = str(year)+str(month)+str(day)+"_"+str(hour)+str(minute)
		htmlPath = os.path.join(path,"bugInfo.html")
		with open(htmlPath, 'w') as fp:
			fp.write(html)
def main(argv):
    bugDataList = []
    rootFolder = ""
    __url = "http://jira.letv.cn"
    __user = "zhoujine_w"
    __pwd = "123456"
    myJira = JIRA(server=__url,basic_auth=(__user,__pwd))
    for line in open(BugID):
        ID = line.rstrip("\n")
        issue = myJira.issue (ID)
        status = issue.fields.status
        title = issue.fields.summary
        sumbitdate = issue.fields.created[0:10]+" "+issue.fields.created[11:19]
        Assignee = issue.fields.assignee
        Component = issue.fields.components[0]
        bugDataList.append({"ID":ID,"title":title,"status":status,"sumbitdate":sumbitdate,"Assignee":Assignee,"Component":Component})
    HtmlReport(bugDataList).writeToFile(rootFolder)

if __name__ == '__main__':
    main(sys.argv)