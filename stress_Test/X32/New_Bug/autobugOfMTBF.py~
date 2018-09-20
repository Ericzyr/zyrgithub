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
import tarfile
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
LOG_STACK = "/logstack.log"


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
                self.parse_logstack(folder,projectName,buildPath)

    def parse_logstack(self,folder, projectName, buildPath):
        # current case properties
        caseclass = ""
        casestep = ""
        casetitle = ""
        pkg = ""
        log = ""
        errortype = ""
        stepindex = 0


        ########################get the case step and case class and case title#########################

        #######################get data form logcat.log#########################
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
                if stepindex < 15:
                    stepindex += 1
                    line = re.sub(r'INSTRUMENTATION_STATUS: caseStep=\d?\d?\.?', str(stepindex) + '.', line, 1).rstrip()
                    casestep += line + "\n"

            elif line.find("INSTRUMENTATION_STATUS: title=") != -1:  # get case step
                casetitle = line[line.index("INSTRUMENTATION_STATUS: title=")+len("INSTRUMENTATION_STATUS: title="):]

            elif line.find("=Reboot occurred") != -1:
                occurTime = ''
                originalParams = {
                    'bugtype':'Reboot',
                    'errortype':errortype,
                    'caseclass':caseclass,
                    'pkg':pkg,
                    'projectname':projectName,
                    'casetitle':casetitle,
                    'casestep':casestep,
                    'filepath':folder,
                    'buildpath':buildPath,
                    'occurtime':occurTime,
                    'log':log,
                    'casetitle':casetitle,
                }
                self.ifNotRepeatByLocalCheckThenAdd(originalParams)
                return

            elif line.find("=ANR occurred") != -1:
                try:
                    logstack = open(folder + LOG_STACK, "r")
                    logstacklines =logstack.readlines()
                except IOError:
                    logstacklines = ""
                for i, line in enumerate(logstacklines):
                    if line.find(": ANR in") != -1:
                        ###get log,pkg,occurTime###
                        lis = []
                        occurTime = (line.split(" ")[0] + " " + line.split(" ")[1]).split('.')[0]
                        for l in logstacklines[i:i + 100]:
                            if l.find("E/ActivityManager") != -1:
                                # log = log.join(l.split(':')[3:])
                                lis += l.split(':')[3:]
                        for l in logstacklines[i:i + 5]:
                            if l.find("Reason:") != -1:
                                errortype = l.split(": Reason:")[1].split('(')[0].strip()
                        log = ''.join(lis)
                        pkg = line.split(": ANR in")[1].split('(')[0].strip()

                        log = log.replace("'", "").strip()
                        originalParams = {
                            'bugtype': 'ANR',
                            'errortype': errortype,
                            'caseclass': caseclass,
                            'pkg': pkg,
                            'projectname': projectName,
                            'casetitle': casetitle,
                            'casestep': casestep,
                            'filepath': folder,
                            'buildpath': buildPath,
                            'occurtime': occurTime,
                            'log': log,
                            'casetitle': casetitle,
                        }
                    else:
                        occurTime = ""
                        originalParams = {
                            'bugtype': 'ANR',
                            'errortype': errortype,
                            'caseclass': caseclass,
                            'pkg': pkg,
                            'projectname': projectName,
                            'casetitle': casetitle,
                            'casestep': casestep,
                            'filepath': folder,
                            'buildpath': buildPath,
                            'occurtime': occurTime,
                            'log': log,
                            'casetitle': casetitle,
                        }
                    self.ifNotRepeatByLocalCheckThenAdd(originalParams)
                    return

            elif line.find("=FC occurred") != -1:
                try:
                    logstack = open(folder + LOG_STACK, "r")
                    logstacklines =logstack.readlines()
                except IOError:
                    logstacklines = ""
                for i, line in enumerate(logstacklines):
                    if line.find("FATAL EXCEPTION:") != -1:
                        ###get log,pkg,occurTime###
                        occurTime = (line.split(" ")[0] + " " + line.split(" ")[1]).split('.')[0]
                        lis = []
                        for l in logstacklines[i:i + 50]:
                            if l.find("E/") != -1:
                                if l.find('PID:') != -1:
                                    lis += l.split(':')[3:5]
                                else:
                                    lis += l.split(':')[3:]
                        log = ''.join(lis).split(', PID')[0] + '\n' + ''.join(lis).split(', PID')[1]
                        for l in logstacklines[i:i + 2]:
                            pkg = l.split(":")[4].split(",")[0].split(" ")[1].rstrip()
                        for l in logstacklines[i + 2:i + 3]:
                            if l.find("E/") != -1:
                                errortype = l.split(':')[3].strip()

                        # log = log.replace("'","").strip()
                        originalParams = {
                            'bugtype': 'FC',
                            'errortype': errortype,
                            'caseclass': caseclass,
                            'pkg': pkg,
                            'projectname': projectName,
                            'casestep': casestep,
                            'filepath': folder,
                            'buildpath': buildPath,
                            'occurtime': occurTime,
                            'log': log,
                            'casetitle': casetitle,
                        }
                        self.ifNotRepeatByLocalCheckThenAdd(originalParams)
                        return

            elif line.find("=Tombstone occurred") != -1:
                try:
                    logstack = open(folder + LOG_STACK, "r")
                    logstacklines =logstack.readlines()
                except IOError:
                    logstacklines = ""
                for i, line in enumerate(logstacklines):
                    if line.find(": Build fingerprint: ") != -1:
                        occurTime = (line.split(" ")[0] + " " + line.split(" ")[1]).split('.')[0]
                        lis = []
                        print i
                        print line
                        for l in logstacklines[i:i + 80]:
                            print l
                            if l.find('pid:') != -1:
                                print "33333333333333333"
                                pkg = l.split('>>> ')[1].split(' <<<')[0]
                                lis += l.split(",")[2]
                            elif l.find('backtrace:') != -1:
                                lis += l.strip() + '\n'
                            elif l.find('#') != -1:
                                lis += l.strip() + '\n'
                        log = ''.join(lis)
                        log = log.replace("'", "").strip()
                        originalParams = {
                            'bugtype': 'Tombstone',
                            'errortype': errortype,
                            'caseclass': caseclass,
                            'pkg': pkg,
                            'projectname': projectName,
                            'casetitle': casetitle,
                            'casestep': casestep,
                            'filepath': folder,
                            'buildpath': buildPath,
                            'occurtime': occurTime,
                            'log': log,
                            'casetitle': casetitle,
                        }
                    else:
                        occurTime = ""
                        originalParams = {
                            'bugtype': 'Tombstone',
                            'errortype': errortype,
                            'caseclass': caseclass,
                            'pkg': pkg,
                            'projectname': projectName,
                            'casetitle': casetitle,
                            'casestep': casestep,
                            'filepath': folder,
                            'buildpath': buildPath,
                            'occurtime': occurTime,
                            'log': log,
                            'casetitle': casetitle,
                        }
                    self.ifNotRepeatByLocalCheckThenAdd(originalParams)
                    return





    def ifNotRepeatByLocalCheckThenAdd(self, data):
        global num
        num += 1;
        global allBug
        allBug.append(data)


class Jira():

    __url = "http://jira.letv.cn"
    __user = "zhoujine"
    __pwd = "Zhou0303"

    myJira = JIRA(server=__url,basic_auth=(__user,__pwd))

    def checkFromNetWhetherRepeat(self,data):

            components,isEco = self.getComponent(data['pkg'],data['caseclass'])

            if isEco:
                issues = self.myJira.search_issues('project= MOSHARE and reporter =currentUser() and status != closed')
            elif data['projectname'] =='MAX4-55B':
                issues = self.myJira.search_issues('project= IRIS and reporter =currentUser() and status != closed')
            elif data['projectname'] =='928' or data['projectname'] == 'le_x5' or data['projectname'] == 'max_plus':
                issues = self.myJira.search_issues("project= EOS and reporter =currentUser() and status != closed")
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

    def parseBugParameter(self, data,version):

        testPersonName = ''
        testPersonTell = ''
        testPersonEmail = ''

        ###获取初始数据###
        filepath = data['filepath']                 #parse by myself
        bugtype = data['bugtype']                   #parse by myself
        errortype = data['errortype']               #get from logstack.log
        caseclass= data['caseclass']                #get from case.log---INSTRUMENTATION_STATUS: class=
        projectName = data['projectname']           #get from phoneinfo.txt---buildModel
        casetitle = data['casetitle']               #get from case.log
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
            summary =  "["+projectName+":MTBF:"+ casenames + "]" + str(casetitle).strip() + "时" + pkg + "发生FC with " + errortype
            description = "【测试版本】：(实际测试版本以下面的路径为准)" + '\n' + buildPath + '\n\n'\
                          + "【操作步骤】" +"\nMTBF 测试是自动化测试，包含许多应用循环测试（桌面切换，浏览器，下载，图库，乐拍,乐视视频,同步影院,乐搜,下载中心,Live,信号源,乐见桌面,乐视体育等等），其中出问题时在跑下面的case,具体原因还需要开发结合log具体分析。" + '\n' + casestep.rstrip() + "\n\n【实际结果】" + '\n' + log.rstrip()\
                          +'\n\n' + "【期待结果】\n电视不应该发生FC\n\n" +"【联系方式】\n姓名："+testPersonName+"\n电话："+testPersonTell+"\n电子邮箱："+testPersonEmail
        elif bugtype == 'ANR':
            summary = "["+projectName+":MTBF:"+ casenames + "]" + str(casetitle).strip() + "时" + pkg + "发生ANR with " + errortype
            description = "【测试版本】：(实际测试版本以下面的路径为准)" + '\n' + buildPath + '\n\n'\
                          + "【操作步骤】" +"\nMTBF 测试是自动化测试，包含许多应用循环测试（桌面切换，浏览器，下载，图库，乐拍,乐视视频,同步影院,乐搜,下载中心,Live,信号源,乐见桌面,乐视体育等等），其中出问题时在跑下面的case,具体原因还需要开发结合log具体分析。" + '\n' + casestep.rstrip() + "\n\n【实际结果】" + '\n' + log.rstrip()\
                          +'\n\n' + "【期待结果】\n电视不应该发生ANR\n\n" +"【联系方式】\n姓名："+testPersonName+"\n电话："+testPersonTell+"\n电子邮箱："+testPersonEmail
        elif bugtype == 'Tombstone':
            summary = "[" + projectName + ":MTBF:" + casenames + "]" + str(casetitle).strip() + "时" + pkg + "发生tombstone"
            description = "【测试版本】：(实际测试版本以下面的路径为准)" + '\n' + buildPath + '\n\n'\
                          + "【操作步骤】" +"\nMTBF 测试是自动化测试，包含许多应用循环测试（桌面切换，浏览器，下载，图库，乐拍,乐视视频,同步影院,乐搜,下载中心,Live,信号源,乐见桌面,乐视体育等等），其中出问题时在跑下面的case,具体原因还需要开发结合log具体分析。" + '\n' + casestep.rstrip() + "\n\n【实际结果】" + '\n' + log.rstrip()\
                          +'\n\n' + "【期待结果】\n电视不应该发生Tombstone\n\n" +"【联系方式】\n姓名："+testPersonName+"\n电话："+testPersonTell+"\n电子邮箱："+testPersonEmail
        elif bugtype =='Reboot':
            summary = "[" + projectName + ":MTBF:Reboot]" + str(casetitle).strip() + "时" + "发生重启"
            description = "【测试版本】：(实际测试版本以下面的路径为准)" + '\n' + buildPath + '\n\n'\
                          + "【操作步骤】" +"\nMTBF 测试是自动化测试，包含许多应用循环测试（桌面切换，浏览器，下载，图库，乐拍,乐视视频,同步影院,乐搜,下载中心,Live,信号源,乐见桌面,乐视体育等等），其中出问题时在跑下面的case,具体原因还需要开发结合log具体分析。" + '\n' + casestep.rstrip() + "\n\n【实际结果】" + '\n' + "电视重启"\
                          +'\n\n' + "【期待结果】\n电视不应该发生重启\n\n" +"【联系方式】\n姓名："+testPersonName+"\n电话："+testPersonTell+"\n电子邮箱："+testPersonEmail

        # version = buildPath.split("/")[-1]
        versionType = buildPath.split("/")[-1].split("_")[-2]
        components = ''
        ###初始数据处理完毕###

        occurProbability = '10112'
        priorityId = '2'
        type = "Bug"
        createAPP = ''
        uiversion = 'EUI5.8'
        project = ''
        subproject = ''

        fields = {
            'project': {
                'key': project
            },
            'issuetype': {
                'name': type
            },
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
            # ###影响版本###
            'customfield_10984': [{
                'name': version
            }],
            'customfield_12801': [{
                'value': uiversion
            }],
            'customfield_12623': [{
                'value': subproject
            }],
            # 'customfield_10601': '请填写具体状态描述',
            'labels': ['AUTO','MTBF','TEST_BLOCK'],
        }

        if projectName == '938ATV':
            project = 'DEMETER'
            if bugtype =='Reboot':
                components = 'TVBSP_Kernel'
                #fields.update({'labels': ['AUTO','MTBF','TEST_BLOCK'],})
            else:
                components = self.getComponent938(pkg)
            subproject = 'X4-43 US'
            uiversion = 'Android TV M'
            fields.update({
                'project': {
                'key': project
            },
             'customfield_12623': [{
                'value': subproject
            }],
              'customfield_12801': [{
                'value': uiversion
            }],
            'components': [{
            'name': components
            }],
            })
        elif projectName == '938':
            project = 'DEMETER'
            subproject = 'CN-X4-50'
            if bugtype =='Reboot':
                components = 'TVBSP_Kernel'
                #fields.update({'labels': ['AUTO','MTBF','TEST_BLOCK'],})
            else:
                components = self.getComponent938(pkg)
            fields.update({
                'project': {
                'key': project
            },
            'customfield_12623': [{
                'value': subproject
            }],
            'components': [{
            'name': components
            }],
            })
        elif projectName == '928':
            project = 'EOS'
            if bugtype =='Reboot':
                components = 'TVBSP_Kernel'
                #fields.update({'labels': ['AUTO','MTBF','TEST_BLOCK'],})
            else:
                components = self.getComponent928(pkg)
            if product == 'x65Air':
                subproject = 'Max3-65'
            elif product == 'x55Air':
                subproject = '12023'
            del fields['customfield_12801']
            del fields['customfield_12623']
            fields['customfield_12103']=subproject
            fields.update({
                'project': {
                'key': project
            },
            'customfield_12103': [{
                'id': '12023'
            }],
            'components': [{
            'name': components
            }],
            })
        elif projectName == '918':
            project = 'BRANCHUS'
            if bugtype =='Reboot':
                components = 'BSP_Kernel'
                #fields.update({'labels': ['AUTO','MTBF','TEST_BLOCK'],})
            else:
                components = self.getComponent918(pkg)
            del fields['customfield_12801']
            del fields['customfield_12623']
            fields.update({
                'project': {
                'key': project
            },
            'components': [{
            'name': components
            }],
            })
        elif projectName == '8096':
            project = 'IRIS'
            subproject = '超4 Max55 Blade'
            if bugtype =='Reboot':
                components = 'TVBSP_Kernel'
                #fields.update({'labels': ['AUTO','MTBF','TEST_BLOCK'],})
            else:
                components = self.getComponent8096(pkg)
            fields.update({
            'project': {
                'key': project
            },
            'customfield_12623': [{
                'value': subproject
            }],
            'components': [{
            'name': components
            }],
            })
        elif projectName == '8096ATV':
            project = '8096'
            subproject = 'IRIS'
            uiversion = 'Android TV M'
            if bugtype =='Reboot':
                components = 'TVBSP_Kernel'
                #fields.update({'labels': ['AUTO','MTBF','TEST_BLOCK'],})
            else:
                components = self.getComponent8096(pkg)
            fields.update({
            'project': {
                'key': project
            },
            'customfield_12623': [{
                'value': subproject
            }],
            'customfield_12801': [{
                'value': uiversion
            }],
            'components': [{
            'name': components
            }],
            })
        elif projectName == '8094':
            project = 'HERACLES'
            subproject = 'Max4-70'
            if bugtype =='Reboot':
                components = 'TVBSP_Kernel'
                #fields.update({'labels': ['AUTO','MTBF','TEST_BLOCK'],})
            else:
                components = self.getComponent8094(pkg)
            del fields['customfield_12801']
            fields.update({
            'project': {
                'key': project
            },
            'customfield_12623': [{
                'value': subproject
            }],
            'components': [{
            'name': components
            }],
            })
        elif projectName == '8064':
            project = 'TPRJECT'
            if bugtype =='Reboot':
                components = 'TVBSP_Kernel'
                #fields.update({'labels': ['AUTO','MTBF','TEST_BLOCK'],})
            else:
                components = self.getComponent8064(pkg)
            del fields['customfield_12801']
            del fields['customfield_12623']
            fields.update({
            'project': {
                'key': project
            },
            'components': [{
            'name': components
            }],
            })

        print 'filepath:  ',filepath,'\n\n'
        print 'bugtype:  ',bugtype,'\n\n'
        print 'pkg:  ',pkg,'\n\n'
        print 'caseclass:  ',caseclass,'\n\n'
        print 'components:  ',components,'\n\n'
        print 'projectName:  ',projectName,'\n\n'
        print 'casestep:  '+casestep+'\n\n'
        print 'buildPath:  '+buildPath+'\n\n'
        print 'version:  '+version+'\n\n'
        print 'versionType:  '+versionType+'\n\n'
        # print 'log:  '+log+'\n\n'
        print 'casenames:  '+casenames+'\n\n'
        print 'summary:  '+summary+'\n\n'
        print 'description:  '+description+'\n\n'
        print 'createAPP:  '+createAPP+'\n\n'
        print fields
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

    def get_938_pkg_component(self):
        pkg_938_component = {
            r'^com.stv.camera$': 'Le Camera',
            r'^com.android.bluetooth$': 'AB_Bluetooth',
            r'^com.android.calendar$': 'APP-Calendar',
            # r'^com.android.calendar$': 'TVBSP_Kernel',
            r'^/system/bin/mediaserver$': 'AB_Multimedia',
            r'^com.android.browser$': 'APP-Browser',
            r'^com.stv.feedback$': 'APP-Feedback',
            r'^com.letv.leso$': 'APP-Leso',
            r'^com.stv.t2.account$': 'APP-Member account',
            r'^com.android.settings$': 'APP-Settings',
            r'^com.stv.thememanager$': 'APP-Theme',
            r'^com.stv.camera$': 'APP-TV manager',
            r'^com.letv.lecloud.disk$': 'Cloud disk',
            r'^com.stv.downloads$': 'Download center',
            r'^com.stv.filemanager$': 'File management-local storage',
            r'^com.letv.tvos.gamecenter$': 'Game Center',
            r'^com.stv.launcher$': 'Launcher frame',
            r'^com.stv.helper.main$': 'Letv helper',
            r'^com.android.calendar$': 'LetvSuperTV',
            r'^com.android.calendar$': 'LIVE桌面',
            r'^com.stv.music$': 'Music',
            r'^com.android.calendar$': 'MyLeEco',
            r'^com.stv.videohistory$': 'APP-History',
            r'^com.duole.tvos.appstore$': 'Store',
            r'^com.stv.voice$': 'SuperVoice',
            r'^com.letv.tv$': 'TV版',
            r'^com.stv.videoplayer$': 'VideoPlayer',
            r'^com.stv.systemupgrade$': 'AB_Upgrade',
            r'^com.stv.signalsourcemanager$': 'Signal source',
            r'^com.android.gallery3d$': 'APP-Gallery',
            r'^com.stv.weather$': 'APP-Weather',
            r'^com.stv.smartControl$': 'AB_2.4GRemoteControl',
            r'^com.android.systemui$': 'TVBSP_Kernel',
            r'^com.letv.android.tv.letvlive$': 'AndroidTV-LiveTV',
            r'^com.google.android.leanbacklauncher$': 'AndroidTV-GMS',
            r'^com.stv.net.misc$': 'AB_network',
            r'^com.letv.reportService$': 'APP-Feedback',
            r'^com.google.android.music$': 'AndroidTV-GMS',
            r'^com.lesports.tv$': '乐视体育',
            r'^com.netflix.ninja$': 'NetFlix',
        }
        return pkg_938_component

    def get_928_pkg_component(self):
        pkg_928_component = {
            r'^com.stv.camera$': 'Le Camera',
            r'^com.android.bluetooth$': 'AB_Bluetooth',
            r'^com.android.calendar$': 'APP-Calendar',
            r'^com.stv.bootadmanager$': 'AB_kernel',
            r'^/system/bin/mediaserver$': 'AB_Multimedia',
            r'^com.android.browser$': 'Browser',
            r'^com.stv.feedback$': 'Feedback',
            r'^com.letv.leso$': 'APP_Leso',
            r'^com.stv.t2.account$': 'Member account',
            r'^com.android.settings$': '设置--系统设置',
            r'^com.stv.thememanager$': 'APP-Theme',
            #r'$': 'APP-TV manager',
            r'^com.letv.lecloud.disk$': 'Cloud disk',
            r'^com.stv.downloads$': 'Download center',
            r'^com.stv.filemanager$': 'File management-local storage',
            r'^com.letv.tvos.gamecenter$': 'Game Center',
            r'^com.stv.launcher$': 'Launcher',
            r'^com.stv.helper.main$': 'Letv helper',
            r'^com.android.calendar$': 'LetvSuperTV',
            r'^com.stv.music$': 'Music',
            r'^com.android.calendar$': 'MyLeEco',
            r'^com.stv.videohistory$': 'History',
            r'^com.duole.tvos.appstore$': 'LetvStore',
            r'^com.stv.voice$': 'Voice',
            r'^com.letv.tv$': 'TV版',
            r'^com.stv.videoplayer$': 'Video Player',
            r'^com.stv.systemupgrade$': 'APP-System update',
            r'^com.stv.signalsourcemanager$': 'Signal source',
            r'^com.android.gallery3d$': 'Gallery',
            r'^com.stv.weather$': 'Weather',
            r'^com.stv.smartControl$': 'AB_RemoteControl',
            r'^com.android.systemui$': 'AB_System',
            r'^com.letv.android.tv.letvlive$': 'AndroidTV-LiveTV',
            r'^com.google.android.leanbacklauncher$': 'GMS',
            r'^com.stv.net.misc$': 'AB_Network',
            r'^com.letv.reportService$': 'APP-Feedback',
            r'^com.google.android.music$': 'GMS',
            r'^com.lesports.tv$': '乐视体育',
        }
        return pkg_928_component

    def get_8094_pkg_component(self):
        pkg_8094_component = {
            r'^com.stv.camera$': 'AB_Camera',
            r'^com.android.bluetooth$': 'AB_bluetooth',
            r'^com.android.calendar$': 'Calendar',
            # r'^com.android.calendar$': 'TVBSP_Kernel',
            r'^/system/bin/mediaserver$': 'AB_multimedia',
            r'^com.android.browser$': 'Browser',
            r'^com.stv.feedback$': 'Feedback',
            r'^com.letv.leso$': 'APP_Leso',
            r'^com.stv.t2.account$': 'Member account',
            r'^com.android.settings$': 'Settings',
            r'^com.stv.thememanager$': 'APP-Theme',
            #r'$': 'APP-TV manager',
            r'^com.letv.lecloud.disk$': 'Cloud disk',
            r'^com.stv.downloads$': 'Download center',
            r'^com.stv.filemanager$': 'File management-local storage',
            r'^com.letv.tvos.gamecenter$': 'Game Center',
            r'^com.stv.launcher$': 'Launcher',
            r'^com.stv.music$': 'Music',
            r'^com.stv.videohistory$': 'History',
            r'^com.duole.tvos.appstore$': 'Store',
            r'^com.stv.voice$': 'Voice',
            r'^com.letv.tv$': 'LetvSuperTV',
            r'^com.stv.videoplayer$': 'VideoPlayer',
            r'^com.stv.systemupgrade$': 'APP-System update',
            r'^com.stv.signalsourcemanager$': 'Signal source',
            r'^com.android.gallery3d$': 'Gallery',
            r'^com.stv.weather$': 'Weather',
            r'^com.stv.smartControl$': 'AB_Remote control',
            r'^com.android.systemui$': 'AB_System',
            r'^com.google.android.leanbacklauncher$': '3rd APP',
            r'^com.stv.net.misc$': 'AB_network',
            r'^com.letv.reportService$': 'Feedback',
            r'^com.google.android.music$': '3rd APP',
            r'^com.lesports.tv$': 'Launcher-Sport',
        }
        return pkg_8094_component

    def get_8064_pkg_component(self):
        pkg_8064_component = {
            r'^com.stv.camera$': '乐拍',
            r'^com.android.bluetooth$': 'AB_蓝牙',
            r'^com.android.calendar$': 'APP_日历',
            # r'^com.android.calendar$': 'TVBSP_Kernel',
            r'^/system/bin/mediaserver$': 'AB_MultiMedia',
            r'^com.android.browser$': '浏览器',
            r'^com.stv.feedback$': '问题反馈',
            r'^com.letv.leso$': '乐搜',
            r'^com.stv.t2.account$': '乐视账户',
            r'^com.android.settings$': 'X60_Settings',
            #r'$': 'APP-TV manager',
            r'^com.letv.lecloud.disk$': '云盘',
            r'^com.stv.downloads$': '下载中心',
            r'^com.stv.filemanager$': 'File management-local storage',
            r'^com.letv.tvos.gamecenter$': '游戏中心',
            r'^com.stv.launcher$': '桌面',
            r'^com.stv.music$': '音乐播放器',
            r'^com.stv.videohistory$': '播放记录',
            r'^com.duole.tvos.appstore$': 'LetvStore',
            r'^com.stv.voice$': '语音',
            r'^com.letv.tv$': '内部应用预置—乐视TV版',
            r'^com.stv.videoplayer$': '本地播放器',
            r'^com.stv.systemupgrade$': '设置-系统升级',
            r'^com.stv.signalsourcemanager$': 'X60_信号源_BSP',
            r'^com.android.gallery3d$': '图片库',
            r'^com.stv.weather$': '天气',
            r'^com.stv.smartControl$': 'AB_遥控器',
            r'^com.android.systemui$': '系统功能',
            r'^com.stv.net.misc$': 'AB_Network',
            r'^com.letv.reportService$': '问题反馈',
        }
        return pkg_8064_component

    def get_918_pkg_component(self):
        pkg_918_component = {
            r'^com.stv.camera$': 'APP_电视乐拍',
            r'^com.android.calendar$': 'APP_日历',
            r'^/system/bin/mediaserver$': 'BSP_Multimedia',
            r'^com.android.browser$': 'APP_浏览器',
            r'^com.stv.feedback$': 'APP_问题反馈',
            r'^com.letv.leso$': 'APP_乐搜',
            r'^com.stv.t2.account$': 'APP_乐视帐号',
            r'^com.android.settings$': 'APP_设置',
            r'^com.letv.lecloud.disk$': 'APP_云相册',
            r'^com.stv.downloads$': 'APP_下载中心',
            r'^com.stv.filemanager$': 'APP_文件管理',
            r'^com.letv.tvos.gamecenter$': 'APP_游戏中心',
            r'^com.stv.launcher$': '桌面框架',
            r'^com.stv.music$': '音乐播放器',
            r'^com.stv.videohistory$': 'APP_播放记录',
            r'^com.duole.tvos.appstore$': 'APP_LetvStore',
            r'^com.stv.voice$': 'APP_语音助手',
            r'^com.letv.tv$': 'APP_乐视网TV版',
            r'^com.stv.videoplayer$': 'APP_播放器',
            r'^com.stv.systemupgrade$': 'APP_系统更新',
            r'^com.stv.signalsourcemanager$': 'APP_信号源',
            r'^com.android.gallery3d$': 'APP_相册',
            r'^com.stv.weather$': 'APP_天气',
            r'^com.stv.smartControl$': 'BSP_RemoteControl',
            r'^com.android.systemui$': 'APP_系统状态',
            r'^com.stv.net.misc$': 'BSP_Network',
            r'^com.letv.reportService$': '数据上报',
        }
        return pkg_918_component

    def get_8096_pkg_component(self):
        pkg_8096_component = {
            r'^com.stv.camera$': 'Le Camera',
            r'^com.android.bluetooth$': 'AB_bluetooth',
            r'^com.android.calendar$': 'APP-Calendar',
            # r'^com.android.calendar$': 'TVBSP_Kernel',
            r'^/system/bin/mediaserver$': 'AB_multimedia',
            r'^com.android.browser$': 'Browser',
            r'^com.stv.feedback$': 'Feedback',
            r'^com.letv.leso$': 'APP_Leso',
            r'^com.stv.t2.account$': 'Member account',
            r'^com.android.settings$': 'Settings',
            r'^com.stv.thememanager$': 'APP-Theme',
            r'^com.stv.camera$': 'APP-TV manager',
            r'^com.letv.lecloud.disk$': 'Cloud disk',
            r'^com.stv.downloads$': 'Download center',
            r'^com.stv.filemanager$': 'File management-local storage',
            r'^com.letv.tvos.gamecenter$': 'Game Center',
            r'^com.stv.launcher$': 'Launcher',
            r'^com.stv.helper.main$': 'APP-乐视电视助手',
            r'^com.android.calendar$': 'LetvSuperTV',
            r'^com.stv.music$': 'Music',
            r'^com.stv.videohistory$': 'History',
            r'^com.duole.tvos.appstore$': 'Store',
            r'^com.stv.voice$': 'Voice-Lele',
            r'^com.letv.tv$': 'LetvSuperTV',
            r'^com.stv.videoplayer$': 'VideoPlayer',
            r'^com.stv.systemupgrade$': 'APP-System update',
            r'^com.stv.signalsourcemanager$': 'Signal source',
            r'^com.android.gallery3d$': 'Gallary',
            r'^com.stv.weather$': 'Weather',
            r'^com.stv.smartControl$': 'AB_Remote control',
            r'^com.android.systemui$': 'TVBSP_Kernel',
            r'^com.letv.android.tv.letvlive$': 'AndroidTV-LiveTV',
            r'^com.google.android.leanbacklauncher$': 'AndroidTV-GMS',
            r'^com.stv.net.misc$': 'AB_network',
            r'^com.letv.reportService$': 'APP-Feedback',
            r'^com.google.android.music$': 'AndroidTV-GMS',
        }
        return pkg_8096_component

    def getComponent8096(self,pkg):
        pkg_8096_component = self.get_8096_pkg_component()
        for item in pkg_8096_component.keys():
            if re.search(item,pkg):
                components=pkg_8096_component.get(item)
                return components
    def getComponent938(self,pkg):
        pkg_938_component = self.get_938_pkg_component()
        for item in pkg_938_component.keys():
            if re.search(item,pkg):
                components=pkg_938_component.get(item)
                return components
    def getComponent918(self,pkg):
        pkg_918_component = self.get_918_pkg_component()
        for item in pkg_918_component.keys():
            if re.search(item,pkg):
                components=pkg_918_component.get(item)
                return components
    def getComponent928(self,pkg):
        pkg_928_component = self.get_928_pkg_component()
        for item in pkg_928_component.keys():
            if re.search(item,pkg):
                components=pkg_928_component.get(item)
                return components
    def getComponent8064(self,pkg):
        pkg_8064_component = self.get_8064_pkg_component()
        for item in pkg_8064_component.keys():
            if re.search(item,pkg):
                components=pkg_8064_component.get(item)
                return components
    def getComponent8094(self,pkg):
        pkg_8094_component = self.get_8094_pkg_component()
        for item in pkg_8094_component.keys():
            if re.search(item,pkg):
                components=pkg_8094_component.get(item)
                return components

def getFolderList(folder):
    pList = []
    for f in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, f)):
            pList.append(os.path.join(folder, f))
    pList.sort(key=lambda x: os.stat(x).st_ctime)
    print pList
    return pList


def getLoopData(logFolder):
    caseLogList = []
    for folder in os.listdir(logFolder):
        if os.path.isdir(os.path.join(logFolder, folder)):
            caseLogList.append(os.path.join(logFolder, folder))
    caseLogList.sort(key=lambda x: os.stat(x).st_ctime)
    print caseLogList
    _p = LogParser(caseLogList)
    print _p
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
        product = ""
        phoneExeTime = 0
        for line in lines:
            if line.find("buildVersion==") != -1:  # get build version
                index = len("buildVersion==")
                phoneVer = line[index:].rstrip()
            if line.find("projectname==") != -1:  # get build version
                index = len("projectname==")
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
            elif line.find("product==") != -1:  # get build date
                index = len("product==")
                product = line[index:].rstrip()
            elif line.find("testStartTime==") != -1:  # get start time
                index = len("testStartTime==")
                startTime = line[index:].rstrip()
            elif line.find("testEndTime==") != -1:  # get end time
                index = len("testEndTime==")
                endTime = line[index:].rstrip()
        #startDateTime = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
        #endDateTime = datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
        startDateTime = 111
        endDateTime = 222
        phoneExeTime = 333
        phoneExeTime = round(phoneExeTime, 1)
        return phoneVer, phoneIMEI, phoneDate, startTime, endTime, phoneExeTime, projectName, buildPath ,versionpath,product

def main(argv):
    rootFolder = argv[1]
    phoneList = getFolderList(rootFolder)

    for phone in phoneList:
        cPhone = phone.split("/")[-1]
        global projectName,buildPath,versionpath,product
        phoneVer, phoneIMEI, phoneDate, phoneStartTime, phoneEndTime, phoneExeTime, projectName, buildPath ,versionpath,product= getBuildInfo(
            rootFolder + "/" + cPhone)

        loopList = getFolderList(phone)
        for loop in loopList:
            getLoopData(loop)

    myJira = Jira()
    global allBug
    print allBug


    for bug in allBug:

        fields = myJira.parseBugParameter(bug,phoneVer)
        #创建bug
        key = myJira.createIssue(fields)
        #添加log到附件并且添加comments
        logName = phoneVer.split("_")[0]+"_"+bug['filepath'].split(os.sep)[-1]
        os.system('cd ' + bug['filepath'] + ' && zip -r '+logName+'.zip ./*')
        logPath = bug['filepath']+'/'+logName+'.zip'
        if os.path.getsize(logPath)<30000000:
            myJira.addAttachment(key,logPath)
            comment = '添加log至附件: '+logName+'.zip'
            myJira.addComments(key,comment)
        else:
            os.system('smbclient //cmsmb.letv.cn/jiralog/ -c "cd TV-MTBF;put '+ logPath +' '+logName+'.zip" -N')
            comment = 'log下载地址为：cmsmb.letv.cn/jiralog/TV-MTBF/'+logName+'.zip'
            myJira.addComments(key,comment)

# #    global num
# #   print "\nall count: "+str(num)
# #    print len(allBug)
#     sendMail(rootFolder)

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
    username = 'zhoujine@letv.com'
    password = 'Zhou0202'

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

