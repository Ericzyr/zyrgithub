#! /usr/bin/env python
# -*- coding: utf-8 -*-  
from __future__ import division
from datetime import datetime
import json
import os
import re
import sys
import django
from datetime import datetime
from django import template
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from jira import JIRA
from django.template.loader import get_template
import gzip
from django.conf import settings
settings.configure(
    DEBUG = False,
    TEMPLATE_DEBUG = False,
	TEMPLATE_DIRS = (os.path.join(os.path.dirname(os.path.abspath(__file__)), 'htmlTemplate'),),
    TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'htmlTemplate')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
)
djangoVersion = django.get_version()[0:3]
if djangoVersion >= '1.7':
    django.setup()


reload(sys)
sys.setdefaultencoding('utf-8')

#########################define global variable#####################
LOG_SUFFIX = "/case.log"
LOG_CAT = "/logcat.log"
DROP_BOX = "dropbox"
FLAG_PASS = "OK (1 test)"


######################################################################

allBug = []
bugidlist = []
num=0
tombstonenum=0
fcnum=0
anrnum=0



class LogParser():

    def __init__(self, folderlist):

        for folder in folderlist:
            str1 = ''
            str1 = str1.join(folder.split("/")[3:])
            if 'test' in str1:
                self.parse_dropbox(folder, projectName, buildPath)
                # self.parse_logcat(folder,projectName,buildPath)

    def parse_dropbox(self, folder, projectName, buildPath):
        # current case properties
        caseclass = ""
        casestep = ""
        pkg = ""
        stepindex = 0

        ########################get the case step and case class#########################
        try:
            logfile = open(folder + LOG_SUFFIX, "r")
            lines = logfile.readlines()
        except IOError:
            lines = ""
            lines_logcat = ""
        # get case dir
        for line in lines:
            if line.find("INSTRUMENTATION_STATUS: class=") != -1:  # get case class
                index = len("INSTRUMENTATION_STATUS: class=")
                caseclass = line[index:].rstrip()

            elif line.find("INSTRUMENTATION_STATUS: caseStep=") != -1:  # get case step
                stepindex += 1
                line = re.sub(r'INSTRUMENTATION_STATUS: caseStep=\d?\d?\.?', str(stepindex) + '.', line, 1).rstrip()
                casestep += line + "\n"


        ########################get data form dropbox#########################
        dropboxpath = os.path.join(folder,DROP_BOX)
        if os.path.exists(dropboxpath):
            file = os.popen('find '+ dropboxpath+' -name "*app_crash@*" -print').readlines()
            if file!=[]:
                for f in file:
                    f = f.strip()
                    time = f.split('@')[1].split('.')[0][:-3]
                    occurTime = os.popen('date -d @'+time+' +%T').readlines()[0].strip()

                    app_crash = open(f, "r")
                    blocks = app_crash.read().split('\n\n')
                    log = '\n\n'.join(blocks[0:2])
                    app_crash.seek(0)
                    lines = app_crash.readlines()
                    for line in lines:
                        if line.find('Process: ') != -1:
                            pkg = line.split('Process: ')[1].strip()
                            break

                    log = log.replace("'","").strip()
                    originalParams = {
                        'bugtype':'FC',
                        'caseclass':caseclass,
                        'pkg':pkg,
                        'projectname':projectName,
                        'casestep':casestep,
                        'filepath':folder,
                        'buildpath':buildPath,
                        'occurtime':occurTime,
                        'log':log,
                    }
                    self.ifNotRepeatByLocalCheckThenAdd(originalParams)


            file = os.popen('find '+ dropboxpath+' -name "*TOMBSTONE@*" -print').readlines()
            if file!=[]:
                for f in file:
                    f = f.strip()
                    time = f.split('@')[1].split('.')[0][:-3]
                    occurTime = os.popen('date -d @'+time+' +%T').readlines()[0].strip()
                    if not f.endswith('gz'):
                        tombstone_file = open(f, "r")
                        blocks = tombstone_file.read().split('\n\n')
                        log = '\n\n'.join(blocks[1:3])
                        tombstone_file.seek(0)
                        lines = tombstone_file.readlines()
                        for line in lines:
                            if line.find('pid: ') != -1:
                                pkg = line.split('>>> ')[1].split(' <<<')[0].strip()
                                break

                    else:
                        tombstone_file = gzip.open(f,'r')
                        blocks = tombstone_file.read().split('\n\n')
                        log = '\n\n'.join(blocks[1:3])
                        tombstone_file.seek(0)
                        lines = tombstone_file.readlines()
                        for line in lines:
                            if line.find('pid: ') != -1:
                                pkg = line.split('>>> ')[1].split(' <<<')[0].strip()
                                break

                    originalParams = {
                            'bugtype':'Tombstone',
                            'caseclass':caseclass,
                            'pkg':pkg,
                            'projectname':projectName,
                            'casestep':casestep,
                            'filepath':folder,
                            'buildpath':buildPath,
                            'occurtime':occurTime,
                            'log':log,
                        }
                    self.ifNotRepeatByLocalCheckThenAdd(originalParams)

            file = os.popen('find '+ dropboxpath+' -name "*native_crash@*" -print').readlines()
            if file !=[]:
                for f in file:
                    f = f.strip()
                    time = f.split('@')[1].split('.')[0][:-3]
                    occurTime = os.popen('date -d @'+time+' +%T').readlines()[0].strip()
                    if not f.endswith('gz'):
                        tombstone_file = open(f, "r")
                        blocks = tombstone_file.read().split('\n\n')
                        log = '\n\n'.join(blocks[1:3])

                        tombstone_file.seek(0)
                        lines = tombstone_file.readlines()
                        for line in lines:
                            if line.find('pid: ') != -1:
                                pkg = line.split('>>> ')[1].split(' <<<')[0].strip()
                                break

                    else:

                        tombstone_file = gzip.open(f,'r')
                        blocks = tombstone_file.read().split('\n\n')
                        log = '\n\n'.join(blocks[1:3])

                        tombstone_file.seek(0)
                        lines = tombstone_file.readlines()
                        for line in lines:
                            if line.find('pid: ') != -1:
                                pkg = line.split('>>> ')[1].split(' <<<')[0].strip()
                                break

                    originalParams = {
                            'bugtype':'Tombstone',
                            'caseclass':caseclass,
                            'pkg':pkg,
                            'projectname':projectName,
                            'casestep':casestep,
                            'filepath':folder,
                            'buildpath':buildPath,
                            'occurtime':occurTime,
                            'log':log,
                        }
                    self.ifNotRepeatByLocalCheckThenAdd(originalParams)


            file = os.popen('find '+ dropboxpath+' -name "*app_anr@*" -print').readlines()
            if file!=[]:
                for f in file:
                    f = f.strip()
                    time = f.split('@')[1].split('.')[0][:-3]
                    occurTime = os.popen('date -d @'+time+' +%T').readlines()[0].strip()
                    if not f.endswith('gz'):
                        tombstone_file = open(f, "r")
                        blocks = tombstone_file.read().split('\n\n')
                        log = '\n\n'.join(blocks[0:2])

                        tombstone_file.seek(0)
                        lines = tombstone_file.readlines()
                        for line in lines:
                            if line.find('Process: ') != -1:
                                pkg = line.split('Process: ')[1].strip()
                            break

                    else:

                        tombstone_file = gzip.open(f,'r')
                        blocks = tombstone_file.read().split('\n\n')
                        log = '\n\n'.join(blocks[0:2])

                        tombstone_file.seek(0)
                        lines = tombstone_file.readlines()
                        for line in lines:
                            if line.find('Process: ') != -1:
                                pkg = line.split('Process: ')[1].strip()
                            break

                    originalParams = {
                            'bugtype':'ANR',
                            'caseclass':caseclass,
                            'pkg':pkg,
                            'projectname':projectName,
                            'casestep':casestep,
                            'filepath':folder,
                            'buildpath':buildPath,
                            'occurtime':occurTime,
                            'log':log,
                        }
                    self.ifNotRepeatByLocalCheckThenAdd(originalParams)

            # bootfile = os.popen('find '+ dropboxpath+' -name "*BOOT@*" -print').readlines()
            # restartfile = os.popen('find '+ dropboxpath+' -name "*RESTART@*" -print').readlines()
            # if bootfile!=[] or restartfile !=[]:
            #     if bootfile!=[]:
            #         for f in bootfile:
            #             f = f.strip()
            #             time = f.split('@')[1].split('.')[0][:-3]
            #             occurTime = os.popen('date -d @'+time+' +%T').readlines()[0].strip()
            #     elif restartfile!=[]:
            #         for f in restartfile:
            #             f = f.strip()
            #             time = f.split('@')[1].split('.')[0][:-3]
            #             occurTime = os.popen('date -d @'+time+' +%T').readlines()[0].strip()
            #
            #     originalParams = {
            #         'bugtype':'Reboot',
            #         'caseclass':caseclass,
            #         'projectname':projectName,
            #         'casestep':casestep,
            #         'filepath':folder,
            #         'buildpath':buildPath,
            #         'occurtime':occurTime,
            #         'log':'',
            #         'pkg':'',
            #
            #     }
            #
            #     self.ifNotRepeatByLocalCheckThenAdd(originalParams)


    def parse_logcat(self,folder, projectName, buildPath):
        # current case properties
        caseclass = ""
        casestep = ""
        pkg = ""
        stepindex = 0


        ########################get the case step and case class#########################
        try:
            logfile = open(folder + LOG_SUFFIX, "r")
            lines = logfile.readlines()
        except IOError:
            lines = ""
        for line in lines:
            if line.find("INSTRUMENTATION_STATUS: class=") != -1:  # get case class
                index = len("INSTRUMENTATION_STATUS: class=")
                caseclass = line[index:].rstrip()

            elif line.find("INSTRUMENTATION_STATUS: caseStep=") != -1:  # get case step
                stepindex += 1
                line = re.sub(r'INSTRUMENTATION_STATUS: caseStep=\d?\d?\.?', str(stepindex) + '.', line, 1).rstrip()
                casestep += line + "\n"



        #######################get data form logcat.log#########################
        try:
            logfile = open(folder + LOG_CAT, "r")
            lines = logfile.readlines()
        except IOError as e:
            lines = ""
        # filepath = data['filepath']                 #parse by myself
        # bugtype = data['bugtype']                   #parse by myself
        # caseclass= data['caseclass']                #get from case.log---INSTRUMENTATION_STATUS: class=
        # projectName = data['projectname']           #get from phoneinfo.txt---buildModel
        # casestep = data['casestep']                 #get from case.log---INSTRUMENTATION_STATUS: casestep=
        # buildPath = data['buildpath']               #get from buildinfo.txt---buildPath
        # log = (str( data['log'])).replace("'","")   #get from dropbox or logcat.log
        # pkg = data['pkg']                           #parse by myself
        # occurTime = data['occurtime']               #get from dropbox(file name) or logcat.log
        for i, line in enumerate(lines):
            if line.find("FATAL EXCEPTION:") != -1:
                ###get log,pkg,occurTime###
                occurTime = (line.split(" ")[0] + " " + line.split(" ")[1]).split('.')[0]
                lis = []
                for l in lines[i:i + 50]:
                    if l.find("E/") != -1:
                        if l.find('PID:') != -1:
                            lis += l.split(':')[3:5]
                        else:
                            lis += l.split(':')[3:]
                log = ''.join(lis).split(', PID')[0]+'\n'+''.join(lis).split(', PID')[1]
                for l in lines[i:i + 2]:
                    pkg = l.split(":")[4].split(",")[0].split(" ")[1].rstrip()


                log = log.replace("'","").strip()
                originalParams = {
                    'bugtype':'FC',
                    'caseclass':caseclass,
                    'pkg':pkg,
                    'projectname':projectName,
                    'casestep':casestep,
                    'filepath':folder,
                    'buildpath':buildPath,
                    'occurtime':occurTime,
                    'log':log,
                }
                self.ifNotRepeatByLocalCheckThenAdd(originalParams)



            if line.find(": Build fingerprint: ") != -1:
                ###get log,pkg,occurTime###
                occurTime = (line.split(" ")[0] + " " + line.split(" ")[1]).split('.')[0]
                lis = []
                for l in lines[i:i + 50]:
                    if l.find('pid:') != -1:
                        pkg = l.split('>>> ')[1].split(' <<<')[0]
                        lis += l.split(",")[2]
                    elif l.find('backtrace:') != -1:
                        lis +=l.split(':')[3:]
                    elif l.find('#') != -1:
                        lis +=l.split(':')[3:]
                log = ''.join(lis)

                log = log.replace("'","").strip()
                originalParams = {
                    'bugtype':'Tombstone',
                    'caseclass':caseclass,
                    'pkg':pkg,
                    'projectname':projectName,
                    'casestep':casestep,
                    'filepath':folder,
                    'buildpath':buildPath,
                    'occurtime':occurTime,
                    'log':log,
                }
                self.ifNotRepeatByLocalCheckThenAdd(originalParams)



            if line.find(": ANR in") != -1:
                ###get log,pkg,occurTime###
                lis = []
                occurTime = (line.split(" ")[0] + " " + line.split(" ")[1]).split('.')[0]
                for l in lines[i:i + 100]:
                    if l.find("E/ActivityManager") != -1:
                        # log = log.join(l.split(':')[3:])
                        lis += l.split(':')[3:]
                log = ''.join(lis)
                pkg = line.split(": ANR in")[1].split('(')[0].strip()

                log = log.replace("'","").strip()
                originalParams = {
                    'bugtype':'ANR',
                    'caseclass':caseclass,
                    'pkg':pkg,
                    'projectname':projectName,
                    'casestep':casestep,
                    'filepath':folder,
                    'buildpath':buildPath,
                    'occurtime':occurTime,
                    'log':log,
                }
                self.ifNotRepeatByLocalCheckThenAdd(originalParams)


    def ifNotRepeatByLocalCheckThenAdd(self, data):
        global num
        num += 1;
        global allBug
        allBug = list(allBug)
        repeat = False
        bugtype = data['bugtype']
        for bug in allBug:
            #如果bugtype不同直接与下一个进行对比
            if bug['bugtype'] != bugtype:
                continue

            if bugtype == 'FC' or bugtype == 'Tombstone':
                #进行log对比，
                datalog = str(data['log']).split('\n\n')[1].split('\n')
                buglog = str(bug['log']).split('\n\n')[1].split('\n')


                if len(datalog)<len(buglog):
                    minnum = len(datalog)
                else:
                    minnum = len(buglog)

                samelinenum=0
                for i in range(minnum):
                    if datalog[i] == buglog[i]:
                        samelinenum += 1

                #如果包名和log对比都通过则判断相同
                if data['pkg'] == bug['pkg']\
                    and samelinenum>5:

                    repeat = True
                    break
                pass
            elif bugtype == 'ANR':
                #anr是特殊情况

                datalog = str(data['log']).split('\n\n')[0].split('\n')
                buglog = str(bug['log']).split('\n\n')[0].split('\n')
                for l in datalog:
                    if l.find('Subject:')!=-1:
                        data_subject = l.split('(')[0]
                for l in buglog:
                    if l.find('Subject:')!=-1:
                        bug_subject = l.split('(')[0]


                if data['pkg'] == bug['pkg'] and data_subject ==bug_subject:
                    repeat = True
                    break

            elif bugtype == 'Reboot':
                repeat = False
                break

                # pass
        if not repeat:
            allBug.append(data)


class Jira():

    __url = "http://jira.letv.cn"
    __user = "kongfanjue_w"
    __pwd = "123456"

    myJira = JIRA(server=__url,basic_auth=(__user,__pwd))

    def checkFromNetWhetherRepeat(self,data):

            components,isEco = self.getComponent(data['pkg'],data['caseclass'])

            if isEco:
                issues = self.myJira.search_issues('project= MOSHARE and reporter =currentUser() and status != closed')
            elif data['projectname'] =='x1' or data['projectname'] == 'max1':
                issues = self.myJira.search_issues('project= MOBILEP and reporter =currentUser() and status != closed')
            elif data['projectname'] =='le_x2' or data['projectname'] == 'le_x5' or data['projectname'] == 'max_plus':
                issues = self.myJira.search_issues("project= RUBY and reporter =currentUser() and status != closed")
                # print issues
            elif data['projectname'] =='X3':
                issues = self.myJira.search_issues("project= XIII and reporter =currentUser() and status != closed")
            elif data['projectname'] =='s2_plus':
                issues = self.myJira.search_issues("project= XSIX and reporter =currentUser() and status != closed")
            elif data['projectname'] =='S2':
                issues = self.myJira.search_issues("project= LAFITE and reporter =currentUser() and status != closed")


            for issue in issues:

                if len((issue.fields.description).split('发生'))==1 or len((issue.fields.summary).split(']'))==1:
                    continue

                bugtype = (issue.fields.description).split('发生')[1].split('，log如下：')[0]

                bugpkg = (issue.fields.summary).split(']')[1].split('发生')[0]

                tmpdata = (issue.fields.description).split('log如下：')
                if len(tmpdata) == 1:
                    continue
                # print '包含 log如下：'
                # print str(tmpdata[1]).strip()
                # print data['log']

                #如果bugtype不同直接与下一个进行对比
                if data['bugtype'] != bugtype:
                    print bugtype
                    continue


                if bugtype == 'Tombstone':
                    if len(str(tmpdata[1]).split('\n\n'))==1:
                        continue

                    ##进行log对比，
                    datalog = str(data['log']).split('\n\n')[1].strip().split('\n')
                    buglog = str(tmpdata[1]).split("backtrace:")[1].split('如有问题请联系')[0].strip().split('\n')
                    print datalog[1].strip()
                    print "*********************datalog和buglog对比，上为datalong下为buglog*******************"
                    print buglog[0].strip()
                    if datalog[1].strip() != buglog[0].strip():
                        continue



                    # if len(datalog)<len(buglog):
                    #     print "**************************5555555555555555555*************"
                    #     minnum = len(datalog)
                    # else:
                    #     print "**************************5555555555555555555*************"
                    #     minnum = len(buglog)
                    #
                    # samelinenum=0
                    # for i in range(minnum):
                    #     if datalog[i] == buglog[i]:
                    #         samelinenum += 1
                    #
                    # if samelinenum < minnum-2:
                    #     continue

                    #如果包名和log对比都通过则判断相同
                    if data['pkg'] == bugpkg :

                        data['key'] = issue.key
                        print issue.key
                        return True
                    pass
                elif bugtype == 'FC':
                    # if len(str(tmpdata[1]).split('\n\n'))==1:
                    #     print "**************************55555555555************"
                    #     continue

                    ##进行log对比，
                    datalog = str(data['log']).split('\n\n')[1].strip().split('\n')
                    buglog = str(tmpdata[1]).split('如有问题请联系')[0].strip().split('\n')
                    print datalog[1].strip()
                    print "*********************datalog和buglog对比，上为datalong下为buglog*******************"
                    print buglog[6].strip()

                    if datalog[1].strip() != buglog[6].strip():
                        continue
                    if data['pkg'] == bugpkg :

                        data['key'] = issue.key
                        print issue.key
                        return True
                    pass
                elif bugtype == 'ANR':
                    print 'ANRANRANRANR'
                    #anr是特殊情况

                    datalog = str(data['log']).split('\n\n')[0].split('\n')
                    buglog = str(tmpdata[1]).split('\n\n')[0].split('\n')
                    for l in datalog:
                        if l.find('Subject:')!=-1:
                            data_subject = l.split('(')[0]
                    for l in buglog:
                        if l.find('Subject:')!=-1:
                            bug_subject = l.split('(')[0]


                    if data['pkg'] == bugpkg and data_subject ==bug_subject:
                        data['key'] = issue.key
                        return True


                if str(tmpdata[1]).strip() == data['log']:
                    data['key'] = issue.key
                    return True

            return False

    def createIssue(self, fields):
        data = {'fields':fields}

        command = 'curl -D- -u ' + self.__user + ':' + self.__pwd + ' -X POST  --data \'' + json.dumps(data) + '\' -H "Content-Type: application/json" ' + self.__url + '/rest/api/2/issue/'

        print command
        lastLine = ''
        for string in os.popen(command).readlines():
            lastLine = string
            print lastLine
        key = lastLine.split("\"key\":")[1].split(',')[0]
        return key


    def searchIssues(self, jql):
        command = 'curl -D- -u ' + self.__user + ':' + self.__pwd \
                  + ' -X GET -H "Content-Type: application/json" ' \
                  + self.__url + '/rest/api/2/search?jql=' + jql
        print command
        os.system(command)


    def addComments(self, issueKey, comments):
        command = 'curl -D- -u ' + self.__user + ':' + self.__pwd \
                  + ' -X PUT --data \'{"update": { "comment": [{ "add": { "body":"' \
                  + comments + '"}}]}}\' -H "Content-Type: application/json" ' \
                  + self.__url + '/rest/api/2/issue/' + issueKey
        print command
        os.system(command)


    def deleteIssueByKey(self, issueKey):
        command = 'curl -D- -u ' + self.__user + ':' + self.__pwd \
                  + ' -X DELETE -H "Content-Type: application/json" ' \
                  + self.__url + '/rest/api/2/issue/' + issueKey
        print command
        return os.system(command)


    def addAttachment(self, issueKey, filepath):

        command = 'curl -D- -u ' + self.__user + ':' + self.__pwd \
                  + ' -X POST -H "X-Atlassian-Token: nocheck"  -F "file=@' \
                  + filepath +'" '+ self.__url + '/rest/api/2/issue/' + issueKey \
                  + '/attachments'
        print command
        return os.system(command)

    def getIssue(self, issueKey):
        command = 'curl -D- -u ' + self.__user + ':' + self.__pwd \
                  + ' -X GET -H "Content-Type: application/json" ' \
                  + self.__url + '/rest/api/2/issue/' + issueKey
        print command
        return os.system(command)

    def getIssueStatus(self,issueKey):
        issue = self.myJira.issue(issueKey)
        summary= str(issue.raw['fields']['summary'])
        status= str(issue.raw['fields']['status']).split("u'")[-1].split("'")[0]
        assignee= str(issue.raw['fields']['assignee']).split("u'")[-2]
        if str(issue.raw['fields']['resolution'])=="None":
            resolution= "Unresolved"
        else:
            resolution= str(issue.raw['fields']['resolution']).split("u'")[6]#.split("'")[0]
        return issue,summary,status,assignee,resolution

    def parseBugParameter(self, data):

        testPersonName = '刘佳恒'
        testPersonTell = '15510616098'
        testPersonEmail = 'ext-jiaheng.liu@letv.com'

        ###获取初始数据###
        filepath = data['filepath']                 #parse by myself
        bugtype = data['bugtype']                   #parse by myself
        caseclass= data['caseclass']                #get from case.log---INSTRUMENTATION_STATUS: class=
        projectName = data['projectname']           #get from phoneinfo.txt---buildModel
        casestep = data['casestep']                 #get from case.log---INSTRUMENTATION_STATUS: casestep=
        buildPath = data['buildpath']               #get from buildinfo.txt---buildPath
        log = (str( data['log'])).replace("'","")   #get from dropbox or logcat.log
        pkg = data['pkg']                           #parse by myself
        occurTime = data['occurtime']               #get from dropbox(file name) or logcat.log

        ###对初始数据进行处理###
        casenames = pkg.split('.')[-1].strip()
        summary = ''
        description = ''
        rebootname = caseclass.split('.')[-1]

        if bugtype == 'FC':
            summary =  "["+projectName+":autoSmoke:"+ casenames+"]"+ pkg +"发生FC"
            description = "测试版本：" + buildPath.split("/")[-1] + '\n' + "测试机：" + projectName + '\n'\
                          + "【操作步骤】" + '\n' + casestep.rstrip() + "\n\n发生FC，log如下：" + '\n\n' + log.rstrip()\
                          +'\n'+"如有问题请联系\n姓名："+testPersonName+"\n电话："+testPersonTell+"\n电子邮箱："+testPersonEmail
        elif bugtype == 'ANR':
            summary = "["+projectName+":autoSmoke:"+ casenames+"]"+ pkg +"发生ANR"
            description = "测试版本：" + buildPath.split("/")[-1] + '\n' + "测试机：" + projectName + '\n'\
                          + "【操作步骤】" + '\n' + casestep.rstrip() + "\n\n发生ANR，log如下：" + '\n\n' + log.rstrip()\
                          +'\n'+"如有问题请联系\n姓名："+testPersonName+"\n电话："+testPersonTell+"\n电子邮箱："+testPersonEmail
        elif bugtype == 'Tombstone':
            summary = "[" + projectName + ":autoSmoke:" + casenames + "]" + pkg + "发生Tombstone"
            description = "测试版本：" + buildPath.split("/")[-1] + '\n' + "测试机：" + projectName + '\n'\
                          + "【操作步骤】" + '\n' + casestep.rstrip() + "\n\n发生Tombstone，log如下：" + '\n\n' + log.rstrip()\
                          +'\n'+"如有问题请联系\n姓名："+testPersonName+"\n电话："+testPersonTell+"\n电子邮箱："+testPersonEmail
        elif bugtype =='Reboot':
            summary = "[" + projectName + ":autoSmoke:Reboot]" + rebootname + "发生Reboot"
            description = "测试版本：" + buildPath.split("/")[-1] + '\n' + "测试机：" + projectName + '\n'\
                          + "【操作步骤】" + '\n' + casestep.rstrip() + "\n\n发生Reboot\n如有问题请联系\n姓名："\
                          +testPersonName+"\n电话："+testPersonTell+"\n电子邮箱："+testPersonEmail

        version = buildPath.split("/")[-1]
        versionType = buildPath.split("/")[-1].split("_")[-2]
        components,isEco = self.getComponent(pkg,caseclass)
        ###初始数据处理完毕###

        occurProbability = '10112'
        priorityId = '2'
        type = "Bug"
        createAPP = ''

        if isEco and bugtype !='Reboot':
            # for line in os.popen('adb -s '+device +' shell dumpsys package ' + data['pkg']).readlines():
            #     if line.find('versionName=') != -1:
            #         versionNum = line.split("versionName=")[1].rstrip()
            command = "cat "+'/'.join(str(filepath).split('/')[:-2])+"/appinfo.txt | grep -A 1 com.letv.android.phonecontrol | awk -F= '{print $2}'"
            try:
                result = os.popen(command).read().strip()
            except:
                pass
            print result
            if(result != ''):
                versionNum = result
            createAPP = components + '_' + versionNum

        ################一时没看明白丹红想要干什么，反正也不会执行到，先注释了
        # elif isEco and bugtype == 'Reboot':
        #     b = []
        #     jira = self.myJira.project('MOSHARE')
        #     varComponents = components+u'.*'
        #     regex = re.compile(varComponents)
        #     versions = self.myJira.project_versions(jira)
        #
        #     for ver in versions:
        #         if regex.search(ver.name):
        #             b.append(ver.name)
        #
        #
        #     createAPP = b[len(b)-1]

        fields = {
            'summary': summary,
            'customfield_10111': {
                'id': occurProbability
            },
            'components': [{
                'name': components
            }],
            'priority': {
                'id': priorityId
            },
            # ###创建版本###
            'versions': [{
                'name': version
            }],
            'description': description,
            'issuetype': {
                'name': type
            },
            # ###影响版本###
            'customfield_10984': [{
                'name': version
            }],
            'customfield_12109': occurTime,
            'customfield_10601': '请填写具体状态描述',
            'labels': ['auto'],
        }

        ###versionType###
        if versionType == 'netcom':
            versionType = '全网通'
        elif versionType == 'open':
            versionType = 'open'

        if isEco:
            ###phonemodel###
            if projectName == 'x1':
                phonemodel = 'CN_X1_MSM8994'
            elif projectName == 'le_x2':
                phonemodel = 'CN_X2_MSM8996'
            elif projectName == 'X3':
                phonemodel = 'CN_X3_MTK6795'
            elif projectName == 's2_plus':
                phonemodel = 'CN_X6_MTK6797'
            elif projectName == 'max1':
                phonemodel = 'CN_MAX1_MSM8994'
            elif projectName == 'le_x5':
                phonemodel = 'CN_X5_MSM8996'
            elif projectName == 'max_plus':
                phonemodel = 'CN_MAX+_MSM8996'
            elif projectName == 'S2':
                phonemodel = 'CN_S2_MSM8976'

            ###删除非生态的fields###
            del fields['customfield_10984']
            del fields['customfield_12109']
            del fields['customfield_10601']
            del fields['labels']
            del fields['versions']

            fields.update({
                'project': {
                    'key': "MOSHARE"
                },
                'customfield_12611': [{
                    'value': phonemodel
                }],
                # 12751[APP验收测试], 12752[手机ROM测试]
                'customfield_12612': {
                    'id': '12752'
                },
                'customfield_12613': [{
                    'name': createAPP
                }],
                'customfield_12614': [{
                    # 'name':cteateROM
                    'name': version
                }],
                'customfield_10601': '请填写具体状态描述',
                'labels': ['auto'],
            })
        elif projectName == 'x1' or projectName == 'max1':

            # 12054[8994_平台X1], 12055[8994_MAX1_only], 12306[8994_MAX_IN_only], 12125[8994_X1_NA_only], 12303[8996_MAX+], 12304[8996_MAX2], 12305[8996_X2]

            if projectName == 'x1':
                model = '12054'
            elif projectName == 'max1':
                model = '12055'

            fields.update({
                'project': {
                    'key': "MOBILEP"
                },
                'customfield_12107': [{
                    # 'value':'国内_X1_MSM8994'
                    'value': versionType

                }],
                'customfield_12106': {
                    'id': model
                },
            })
        elif projectName == 'le_x2' or projectName == 'le_x5' or projectName == 'max_plus':

            if projectName == 'le_x2':
                model = '8996_X2'
            elif projectName == 'le_x5':
                model = '8996_X5'
                # versionType = 'open'
            elif projectName == 'max_plus':
                model = '8996_MAX+'
                # versionType = 'open'

            fields.update({
                'project': {
                    'key': "RUBY"
                },
                'customfield_12107': [{
                    'value': versionType

                }],
                'customfield_12402': [{
                    'value': model
                }],
            })
        elif projectName == 'X3' or projectName == 's2_plus':

            if projectName == 'X3':
                fields.update({'project': {
                    'key': "XIII"
                }})
            elif projectName == 's2_plus':
                fields.update({'project': {
                    'key': "XSIX"
                }})
        elif projectName == 'S2':
            fields.update({
                'project': {
                    'key': "LAFITE"
                },
                'customfield_12701': [{
                    'value': '8976_S2_CN'
                }],
            })


        print 'filepath:  '+filepath+'\n\n'
        print 'bugtype:  '+bugtype+'\n\n'
        print 'pkg:  '+pkg+'\n\n'
        print 'caseclass:  '+caseclass+'\n\n'
        print 'components:  '+components+'\n\n'
        print 'projectName:  '+projectName+'\n\n'
        print 'casestep:  '+casestep+'\n\n'
        print 'buildPath:  '+buildPath+'\n\n'
        print 'version:  '+version+'\n\n'
        print 'versionType:  '+versionType+'\n\n'
        # print 'log:  '+log+'\n\n'
        print 'casenames:  '+casenames+'\n\n'
        print 'summary:  '+summary+'\n\n'
        print 'description:  '+description+'\n\n'
        print 'createAPP:  '+createAPP+'\n\n'
        return fields

    def checkVersionAndComponent(self,projectkey,version,components,createAPP=None):
        ##############检测组件和版本是否存在，若不存在，则自行创建（需要账号有权限），需要用到第三方jira库
        versions = self.myJira.project_versions(projectkey)
        components_name = self.myJira.project_components(projectkey)

        componentsHasExists=True
        for c in components_name:
            if components == c.name:
                componentsHasExists=False

        if componentsHasExists:
             self.myJira.create_component(name=components,project=projectkey)

        versionHasExists = False
        appVersionHasExists = False
        for v in versions:
            if version == v.name:
                versionHasExists = True
            if createAPP == v.name:
                appVersionHasExists = True
        if projectkey != 'MOSHARE':
            if not versionHasExists:
                self.myJira.create_version(name=version,project=projectkey)
        else:
            if not appVersionHasExists:
                self.myJira.create_version(name=createAPP,project=projectkey)
            if not versionHasExists:
                self.myJira.create_version(name=version,project=projectkey)

    def get_normal_pkg_component(self):
        normal_pkg_component = {
            r'^com.baidu.input_letv$': 'Input_UI',
            r'^com.android.gallery3d$': 'Gallery_UI',
            r'^com.android.calendar$': 'Calendar_UI',
            r'^com.letv.android.ota$': 'Ota_UI',
            r'^com.dsi.ant.server$': 'Ant',
            r'^com.letv.android.account$': 'My Letv_UI',
            r'^com.letv.android.accountinfo$': 'My Letv_UI',
            r'^com.letv.android.themesettings$': 'Themes_UI',
            r'^com.letv.android.note$': 'Note_UI',
            r'^com.android.music': 'Music_UI',
            r'^com.android.calculator2$': 'Calculator_UI',
            r'^com.android.shell$': 'BugReporter_UI',
            r'^com.letv.android.recorder$': 'Recorder_UI',
            r'^com.stv.stvpush$': '3rd party APP compatibility_UI',
            r'^com.letv.factorymode$': 'BSP_Crash',
            r'^com.android.inputdevices$': 'CTS/GTS_UI',
            r'^com.android.keychain$': 'CTS/GTS_UI',
            r'^com.android.bluetooth$': 'Bluetooth_UI',
            r'^com.letv.bsp.qccrashhandler$': 'background killing_UI',
            r'^com.android.contacts$': 'Contacts&Dialer_UI',
            r'^com.letv.android.phonecontrol$': 'Find phone_UI',
            r'^com.letv.android.setupwizard$': 'SetupWizard_UI',
            r'^com.letv.android.freeflow$': 'My Letv_UI',
            r'^com.letv.android.filemanager$': 'File manager_UI',
            r'^com.android.email$': 'Email_UI',
            r'^com.letv.bugpostbox$': 'BugReporter_UI',
            r'^com.android.systemui$': 'Notification manager_UI',
            r'^com.android.phone$': 'SystemService_UI',
            r'^com.android.mms$': 'SMS_UI',
            r'^com.letv.android.wallpaper$': 'wallpaper_UI',
            r'^com.letv.android.supermanager$': 'SupperManager_UI',
            r'^com.letv.android.cloudservice$': 'LeCloud_UI',
            r'^com.android.dialer$': 'Contacts&Dialer_UI',
            r'^com.letv.leui.schpwronoff$': 'Settings_UI',
            r'^com.letv.android.powercontroller$': 'Power on & off settings_UI',
            r'^com.letv.android.usagestats$': 'SystemService_UI',
            r'^com.qualcomm.qti.services.secureui$': 'SystemService_UI',
            r'^com.android.exchange$': 'System_BSP',
            r'^com.android.documentsui$': 'System_BSP',
            r'^com.android.settings$': 'System_BSP',
            r'^com.letv.android.wallpaperonline$': 'Wallpaper_UI',
            r'^com.letv.android.bugreporter$': 'BugReporter_UI',
            r'^com.android.camera2$': 'Camera_app',
            r'^com.letv.android.voiceassistant$': 'Voiceassistant_UI',
            r'^com.android.launcher3$': 'System_BSP',
            r'^com.lesports.glivesports$': 'LeSports_UI',
            r'^com.quicinc.cne.CNEService$': 'BSP_Kernel',
            r'^com.android.deskclock$': 'Clock_UI',
            r'^com.android.videoplayer$': 'Videoplayer_UI',
            r'^com.letv.android.ecoProvider$': 'SystemService_UI',
            r'^com.android.providers.media$': 'Videoplayer_UI',
            r'^com.letv.android.compass$': 'compass_UI',
            r'^com.android.browser$': 'Browser_UI',
            r'^com.android.incallui$': 'Call_UI',
            r'^/system/bin/patchoat$': 'SystemService_UI',
        }
        return normal_pkg_component

    def get_normal_case_component(self):
        normal_case_component = {
            r'^com.letv.cases.leui.WIFI': 'WiFi_UI',
            r'^com.letv.cases.leui.TD.MOCall$': 'Call_UI',
            r'^com.letv.cases.leui.TD.MMS$': 'SMS_UI',
            r'^com.letv.cases.leui.FDDLTE.MOCall$': 'Call_UI',
            r'^com.letv.cases.leui.FDDLTE.SMS$': 'SMS_UI',
            r'^com.letv.cases.leui.FDDLTE.WebBrowsing$': 'Browser_UI',
            r'^com.letv.cases.leui.IMEI': 'Contacts&Dialer_UI',
            r'^com.letv.cases.leui.LeAccount': 'My Letv_UI',
            r'^com.letv.cases.leui.TDLTE.MOCall$': 'Call_UI',
            r'^com.letv.cases.leui.EmergencyCall': 'Call_UI',
            r'^com.letv.cases.leui.TDLTE.MMS$': 'SMS_UI',
            r'^com.letv.cases.leui.AirPlaneMode.AirplaneMode$': 'Settings_UI',
            r'^com.letv.cases.leui.Settings': 'Settings_UI',
            r'^com.letv.cases.leui.GPS': 'Settings_UI',
            r'^com.letv.cases.leui.MusicPlayer': 'Music_UI',
            r'^com.letv.cases.leui.VideoPlayer': 'Videoplayer_UI',
            r'^com.letv.cases.leui.Notification': 'Notification manager_UI',
            r'^com.letv.cases.leui.LockScreen.LockScreen': 'Camera_UI',
            r'^com.letv.cases.leui.ControlCenter': 'Control center_UI',
            r'^com.letv.cases.leui.multitask': 'Control center_UI',
            r'^com.letv.cases.leui.Desktop': 'Launcher_UI',
            r'^com.letv.cases.leui.BrowserTest': 'Browser_UI',
            r'^com.letv.cases.leui.browser': 'Browser_UI',
            r'^com.letv.cases.leui.Camera': 'Camera_UI',
            r'^com.letv.cases.leui.clock': 'Clock_UI',
            r'^com.letv.cases.leui.Calendar': 'Calendar_UI',
            r'^com.letv.cases.leui.Weather': 'Weather_UI',
            r'^com.letv.cases.leui.WallPaperOnline.WallPaperOnline': 'Wallpaper_UI',
            r'^com.letv.cases.leui.FileManager': 'File manager_UI',
            r'^com.letv.cases.leui.Gallery': 'Gallery_UI',
            r'^com.letv.cases.leui.Feedback': 'BugReporter_UI',
            r'^com.letv.cases.leui.Note': 'Note_UI',
            r'^com.letv.cases.leui.Email': 'Email_UI',
            r'^com.letv.cases.leui.Calculator': 'Calculator_UI',
            r'^com.letv.cases.leui.Download': 'Download manager_UI',
            r'^com.letv.cases.leui.Contact': 'Contacts&Dialer_UI',
            r'^com.letv.cases.leui.Record': 'Recorder_UI',
            # r'^com.letv.cases.leui.Settings': 'LeCloud_UI',
            r'^com.letv.cases.leui.media': 'Videoplayer_UI',
            r'^com.letv.cases.leui.message.Email': 'Email_UI',
            r'^com.letv.cases.leui.message.SMSMMS': 'SMS_UI',
            r'^com.letv.cases.leui.housekeeper': 'SupperManager_UI',
            r'^com.letv.cases.leui.Authorization': 'Settings_UI',
            r'^com.letv.cases.leui.Alarm': 'Clock_UI',
        }
        return normal_case_component

    def get_eco_pkg_component(self):
        eco_pkg_component = {
            r'^sina.mobile.tianqitongletv': '天气通',
            r'^com.baidu.BaiduMap': '百度地图',
            r'^com.letv.android.client': '乐视视频大陆版',
            r'^com.sohu.inputmethod.sogou.leshi': '搜狗输入法',
            r'^com.letv.lesophoneclient': '乐搜大陆版',
            r'^com.letv.letvshop': '商城',
            r'^cn.wps.moffice_eng': 'WPS',
            r'^com.letv.games': '游戏中心',
            r'^com.letv.android.remotecontrol': '遥控器大陆版',
            r'^com.letv.android.letvlive': 'LIVE大陆版',
            r'^com.letv.android.remotedevice': '遥控器大陆版',
            r'^com.letv.app.appstore': 'LeStore_CN',
            r'^com.letv.agnes': 'agens',
            r'^com.letv.android.quicksearchbox': '万象搜索',
            r'^com.sina.weibo': 'Weibo_sina',
            r'^com.letv.android.agent': 'agens',
            r'^com.baidu.map.location': '百度地图',
            r'^com.letv.bbs': '乐迷社区',
            r'^com.lesports.glivesports': '乐视体育',
            r'^com.letv.sarrsdesktop': '乐见大陆版',

        }
        return eco_pkg_component

    def get_eco_case_component(self):
        eco_case_component = {
            r'^com.letv.cases.leui.LetvVideo.LetvVideo': '乐视视频大陆版',
            r'^com.letv.cases.leui.LetvSport.LetvSportApp': '乐视体育',
            r'^com.letv.cases.leui.LeStore': '商城',
            r'^com.letv.cases.leui.LetvLIVE': 'LIVE大陆版',
            r'^com.letv.cases.leui.LetvSport': '乐视体育',
            r'^com.letv.cases.leui.LetvVideo': '乐视视频大陆版',
            r'^com.letv.cases.leui.ecological.LetvVideo': '乐视视频大陆版',
            r'^com.letv.cases.leui.ecological.LetvSportApp': '乐视体育',
            r'^com.letv.cases.leui.ecological.LeSo$': '乐搜大陆版',
            r'^com.letv.cases.leui.ecological.Living$': 'LIVE大陆版',
            r'^com.letv.cases.leui.ecological.LeJian$': '乐见大陆版',
            r'^com.letv.cases.leui.ecological.LeStore': '商城',
            r'^com.letv.cases.leui.ecological.LeKan$': '乐搜大陆版',
            r'^com.letv.cases.leui.weibo': 'Weibo_sina',
            r'^com.letv.cases.leui.lefanbbs': '乐迷社区',
            r'^com.letv.cases.leui.WPS': 'WPS',
            r'^com.letv.cases.leui.gamecenter': '游戏中心',
            r'^com.letv.cases.leui.AppStore': 'LeStore_CN',
            r'^com.letv.cases.leui.ecological.AppStore': 'LeStore_CN',
            r'^com.letv.cases.leui.AppManage': 'LeStore_CN',
            r'^com.letv.cases.leui.Map': '百度地图',
        }
        return eco_case_component

    def getComponent(self,pkg,case):
        normal_case_component = self.get_normal_case_component()
        normal_pkg_component = self.get_normal_pkg_component()
        eco_case_component = self.get_eco_case_component()
        eco_pkg_component = self.get_eco_pkg_component()

        for item in normal_pkg_component.keys():
            if re.search(item,pkg):
                components=normal_pkg_component.get(item)
                return components,False

        for item in eco_pkg_component.keys():
            if re.search(item,pkg):
                components=eco_pkg_component.get(item)
                return components,True

        for item in normal_case_component.keys():
            if re.search(item,case):
                components=normal_case_component.get(item)
                return components,False

        for item in eco_case_component.keys():
            if re.search(item,case):
                components=eco_case_component.get(item)
                return components,True


def getFolderList(folder):
    pList = []
    for f in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, f)):
            pList.append(os.path.join(folder, f))
    pList.sort(key=lambda x: os.stat(x).st_ctime)
    return pList


def getLoopData(logFolder):
    caseLogList = []
    for folder in os.listdir(logFolder):
        if os.path.isdir(os.path.join(logFolder, folder)):
            caseLogList.append(os.path.join(logFolder, folder))
    caseLogList.sort(key=lambda x: os.stat(x).st_ctime)
    _p = LogParser(caseLogList)
    return _p

def getBuildInfo(folder):
        try:
            phoneInfo = open(folder + "/phoneInfo.txt", "r")
            lines = phoneInfo.readlines()
        except IOError as e:
            lines = ""
        phoneVer = ""
        projectName = ""
        phoneIMEI = ""
        buildPath = ""
        versionpath=""
        phoneDate = ""
        startTime = ""
        endTime = ""
        phoneExeTime = 0
        for line in lines:
            if line.find("buildVersion==") != -1:  # get build version
                index = len("buildVersion==")
                phoneVer = line[index:].rstrip()
            if line.find("buildModel==") != -1:  # get build version
                index = len("buildModel==")
                projectName = line[index:].rstrip()
            if line.find("buildPath==") != -1:  # get build version
                index = len("buildPath==")
                buildPath = line[index:].rstrip()
            if line.find("versionpath==") != -1:  # get build version
                index = len("versionpath==")
                versionpath = line[index:].rstrip()
            if line.find("IMEI==") != -1:  # get phoneIMEI
                index = len("IMEI==")
                phoneIMEI = line[index:].rstrip()
            elif line.find("buildDate==") != -1:  # get build date
                index = len("buildDate==")
                phoneDate = line[index:].rstrip()
            elif line.find("testStartTime==") != -1:  # get start time
                index = len("testStartTime==")
                startTime = line[index:].rstrip()
            elif line.find("testEndTime==") != -1:  # get end time
                index = len("testEndTime==")
                endTime = line[index:].rstrip()
        startDateTime = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
        endDateTime = datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
        phoneExeTime = (endDateTime - startDateTime).total_seconds() / 3600
        phoneExeTime = round(phoneExeTime, 1)
        return phoneVer, phoneIMEI, phoneDate, startTime, endTime, phoneExeTime, projectName, buildPath ,versionpath

def main(argv):
    rootFolder = argv[1]
    phoneList = getFolderList(rootFolder)

    for phone in phoneList:
        cPhone = phone.split("/")[-1]
        global projectName,buildPath,versionpath
        phoneVer, phoneIMEI, phoneDate, phoneStartTime, phoneEndTime, phoneExeTime, projectName, buildPath ,versionpath= getBuildInfo(
            rootFolder + "/" + cPhone)

        loopList = getFolderList(phone)
        for loop in loopList:
            getLoopData(loop)

    myJira = Jira()
    global allBug

    for bug in allBug:
        ###以下部分为联网查重###
        if myJira.checkFromNetWhetherRepeat(bug):
            # print '------------------'
            # print bug['pkg']
            # print bug['log']
            # print '------------------'
            #添加附件
            print "××××××××××××××××××××××××××××××××××××××××××××××××××××××××查重成功××××××××××××××××××××××××××××××××××××××"
            bugidlist.append(bug['key'])
            print bugidlist
            logName = bug['filepath'].split(os.sep)[-1]
            os.system('cd ' + bug['filepath'] + ' && zip -r '+logName+'.zip ./*' )
            logPath = bug['filepath']+'/'+logName+'.zip'
            if os.path.getsize(logPath)<30000000:
                myJira.addAttachment(bug['key'],logPath)
                comment = '版本'+bug['buildpath']+'复现,添加log至附件: '+logName+'.zip'
                myJira.addComments(bug['key'],comment)
            else:
                os.system('smbclient //cmsmb.letv.cn/jiralog/ -c "cd autotest;put '+ logPath +' '+logName+'.zip" -N')
                comment = '版本'+bug['buildpath']+'复现\\nlog下载地址为：//cmsmb.letv.cn/jiralog/autotest/'+logName+'.zip'
                myJira.addComments(bug['key'],comment)
            pass
        else:
            pass
            #######################以上部分为联网查重###

            fields = myJira.parseBugParameter(bug)
            #print fields['customfield_12614'][0]['name']
            print "-----------------------"
            #检测组件和版本是否存在，若不存在，则自行创建（需要账号有权限）--暂时注释
            if fields['project']['key'] == 'MOSHARE':
                myJira.checkVersionAndComponent(fields['project']['key'],
                                                fields['customfield_12614'][0]['name'],
                                                fields['components'][0]['name'],
                                                fields['customfield_12613'][0]['name'])
            else:
                myJira.checkVersionAndComponent(fields['project']['key'],
                                                fields['versions'][0]['name'],
                                                fields['components'][0]['name'])
            #创建bug
            key = myJira.createIssue(fields)
            #汇报过的bug记录到一个文件
            # record = open("/home/letv/autoreportbug.txt",'a')
            # record.writelines(key+"\n")
            print "*****************************************buglist**********************************************"
            print key
            bugidlist.append(key.split("\"")[1])
            print bugidlist
            #添加log到附件并且添加comments
            logName = bug['filepath'].split(os.sep)[-1]
            os.system('cd ' + bug['filepath'] + ' && zip -r '+logName+'.zip ./*')
            logPath = bug['filepath']+'/'+logName+'.zip'
            if os.path.getsize(logPath)<30000000:
                myJira.addAttachment(key,logPath)
                comment = '添加log至附件: '+logName+'.zip'
                myJira.addComments(key,comment)
            else:
                os.system('smbclient //cmsmb.letv.cn/jiralog/ -c "cd autotest;put '+ logPath +' '+logName+'.zip" -N')
                comment = '版本'+bug['buildpath']+'复现\\nlog下载地址为：//cmsmb.letv.cn/jiralog/autotest/'+logName+'.zip'
                myJira.addComments(key,comment)

#    global num
#   print "\nall count: "+str(num)
#    print len(allBug)
    sendMail(rootFolder)

######################################################自动发邮件#####################################################

class bug:
    def __init__(self,id,summary,status,assignee,resolution):
        self.id = id
        self.summary = summary
        self.status = status
        self.assignee = assignee
        self.resolution = resolution


#version = 'full_s2_plus_belmont_mp_leui_20160308_HBXCNCU5606105191E_20160519_032440_cu_userdebug'
#versionpath = 'smb://cmsmb.letv.cn/dailybuild/mtk-x6/cn/full_s2_plus/factory/belmont_mp_leui_20160308/20160519/full_s2_plus_belmont_mp_leui_20160308_HBXCNCU5606105191E_20160519_032440_cu_userdebug'
#report = 'http://10.140.60.134:9912/view/TC_Auto/job/TC_X6_Smoke_Test_211/287/artifact/287/index.html'
#phonemodel = 'X2'
def sendMail(rootFolder):
    version = buildPath.split("/")[1]
    mailversionpath = versionpath
    report = "http://10.140.60.134:9912/view/TC_Auto/job/"+rootFolder.split("/")[5]+"/"+rootFolder.split("/")[-1]+"/artifact/"+rootFolder.split("/")[-1]+"/index.html"
    phonemodel = projectName

    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    nowtime = str(year)+"/"+str(month)+"/"+str(day)

    print version
    print mailversionpath
    print report
    print phonemodel


#    sender = 'ext-jiaheng.liu@le.com'
#    receiver = 'tcauto@le.com'
#    username = 'ext-jiaheng.liu@letv.com'
#    password = '!@c20160503'

    sender = 'ext-jiaheng.liu@le.com'
    receiver = 'tcauto@le.com'
    username = 'ext-jiaheng.liu@letv.com'
    password = '!@c20160503'

    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = '【测试中心】【'+phonemodel+'】Smoke自动化冒烟测试: '+ version
    global bugidlist
    mailbuglist = []
    for bugid in bugidlist:
        issue,summary,status,assignee,resolution = Jira().getIssueStatus(bugid)
        mailbuglist.append(bug(issue,summary,status,assignee,resolution))


    passnum=72-len(mailbuglist)
    failnum=len(mailbuglist)
    passrate='%.2f'%(passnum/72*100)+"%"
    rebootrnum=str(os.popen("grep -A1 'Total Reboot' "+rootFolder+"/index.html | cut -d '>' -f3 | cut -d '<' -f1").read()).split("Reboot")[1].strip()
    Functionnum=str(os.popen("grep -A1 'Rack Fault number' "+rootFolder+"/index.html | cut -d '>' -f3 | cut -d '<' -f1").read()).split("number")[1].strip()
    tombstonenum=str(os.popen("grep -A1 'Total Tombstone' "+rootFolder+"/index.html | cut -d '>' -f3 | cut -d '<' -f1").read()).split("Tombstone")[1].strip()
    fcnum=str(os.popen("grep -A1 'Total Force Close' "+rootFolder+"/index.html | cut -d '>' -f3 | cut -d '<' -f1").read()).split("Close")[1].strip()
    anrnum=str(os.popen("grep -A1 'Total ANR' "+ rootFolder+"/index.html | cut -d '>' -f3 | cut -d '<' -f1").read()).split("ANR")[1].strip()
    print tombstonenum
    print fcnum
    print anrnum
    print failnum
    print passnum
    print passrate
    param = {}
    param['version']=version
    param['versionpath']=versionpath
    param['report']=report


#    bug1 = bug('RUBY-16892','【X2_Auto:smoke:相机】 com.android.camera2发生FC','RESOLVED','姜 天宇','Fixed')
#    bug2 = bug('XIII-16552','[X3_012S][MTBF_India] Launch app music, play music and stop play music,the phone occurred FC:com.google.android.googlequicksearchbox:search','TRACK','管 小鹏','Fixed')

    param['buglist']=mailbuglist
    param['passnum'] = passnum
    param['failnum'] = failnum
    param['blocknum'] = '0'
    param['totallynum'] = '72'
    param['passrate'] = passrate
    param['title'] = projectName+'_Smoke Test Report'
    param['date'] =nowtime
    param['tester'] = '刘佳恒'
    param['hw'] = 'PVT2'
    param['sw'] = version
    param['anrnum'] = anrnum
    param['fcnum'] = fcnum
    param['rebootrnum'] = rebootrnum
    param['tombstonenum'] = tombstonenum
    param['Functionnum'] = Functionnum

    t = get_template("mail.html")
    c = template.Context(param)
    # print t.render(c)
    msg = MIMEText(t.render(c),'html', 'utf-8')
    msgRoot.attach(msg)

    # fp = open(rootFolder+'/Phone1/BatteryStatus.csv', 'rb')
    # msgImage = MIMEImage(fp.read())
    # fp.close()
    # msgImage.add_header('Content-ID', '<image1>')
    # msgRoot.attach(msgImage)
    #
    msgText = MIMEText(open(rootFolder+'/Phone1/BatteryStatus.csv', 'rb').read(), 'base64', 'utf-8')
    msgText['Content-Type'] = 'application/octet-stream'
    msgText['Content-Disposition'] = 'attachment; filename="BatteryStatus.csv"'
    # msgMCM = MIMEText(open(rootFolder+'/Phone1/mcm_result/MCM_HTML.zip', 'rb').read(), 'base64', 'utf-8')
    # msgMCM['Content-Type'] = 'application/octet-stream'
    # msgMCM['Content-Disposition'] = 'attachment; filename="MCM_HTML.zip"'
    msgRoot.attach(msgText)
    # msgRoot.attach(msgMCM)

    smtp = smtplib.SMTP()
    try:
        smtp.connect('mail.letv.com')
        smtp.login(username, password)
    except:
        print 'failed to login to smtp server'
    smtp.sendmail(sender, receiver, msgRoot.as_string())
    smtp.quit()



if __name__ == '__main__':
    main(sys.argv)

