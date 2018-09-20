#! /usr/bin/env python
# -*- coding: utf-8 -*-
from jira import JIRA
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
__url = "http://jira.letv.cn"
__user = "kongfanjue_w"
__pwd = "123456"

myJira = JIRA(server=__url,basic_auth=(__user,__pwd))
project = myJira.project("BRANCHUS")
components = myJira.project_components(project)
# print [c.name for c in components]

# for i in components:
#     print i.name


issue = myJira.issue('BRANCHUS-27007')
for field_name in issue.raw['fields']:
    print "Field:", field_name, "Value:", issue.raw['fields'][field_name]


