#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from django.template.loader import get_template
from django import template
import smtplib
from django.conf import settings
import django
import jiratools
import config

settings.configure(
    DEBUG=False,
    TEMPLATE_DEBUG=False,
    TEMPLATE_DIRS=(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'htmlTemplate'),),
    TEMPLATES=[
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

class bug:
    def __init__(self,id,summary,status,assignee,resolution):
        self.id = id
        self.summary = summary
        self.status = status
        self.assignee = assignee
        self.resolution = resolution

class Sendmail():


    def __init__(self, rootFolder, device, bugidlist, funcbuglist, tag):
        self.rootFolder = rootFolder
        self.versionpath = device.versionPath
        self.projectName = device.getProjectName()
        self.bugidlist = bugidlist
        self.funcbuglist = funcbuglist
        self.tag = tag
        self.buildModel = device.buildModel

    def getIssueStatus(self, issueKey):
        issue = jiratools.getMyJira().issue(issueKey)
        summary = issue.raw['fields']['summary']
        status = issue.raw['fields']['status']['name']
        assignee = issue.raw['fields']['assignee']['name']
        if str(issue.raw['fields']['resolution']) == "None":
            resolution = "Unresolved"
        else:
            resolution = issue.raw['fields']['resolution']['name']  # .split("'")[0]
        return issue, summary, status, assignee, resolution

    def sendMail(self):

        # version = 'x450_demeter_V2401RCN01C058204D08101T_20160810_004514_full_userdebug'
        # versionpath = 'smb://imgrepo-cnbj.devops.letv.com/dailybuild/SuperTV/demeter/cn/aosp_mangosteen/daily/20160810/x450_demeter_V2401RCN01C058204D08101T_20160810_004514_full_userdebug'
        # report = 'http://10.148.18.3:9912/view/06.TestCenter/view/Auto-Test/job/TC-X50-Auto-Test/23/artifact/23/2016810_1149.html'
        # phonemodel = 'Max3-65'


        version = self.versionpath.split("/")[-1]

        phonemodel = self.projectName

        if self.tag == True:
            testType = 'Smoke'
        else :
            testType = 'Sanity'


        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        nowtime = str(year) + "/" + str(month) + "/" + str(day)

        # print version
        # print self.versionpath
        # print phonemodel
        jenkinsServer = "http://cim.devops.letv.com"
        sender = 'tcautobuildsystem@le.com'
        if phonemodel == 'TV_928' or phonemodel == 'TV_938':
            hw = self.buildModel
            # receiver = ['ext-danhong_zhang@le.com']
            receiver = ['tcauto@le.com','letv_spm_tv@le.com','zhanghongliang1@le.com','Letv_TV_Test@le.com','yanggaochuang@le.com','zhaofang@le.com','calvin.wong@le.com','xiaoying@le.com','tongyonghui@le.com','guochunjing@le.com','letv_sqa@le.com','letv_spm@le.com','qihongbin@le.com','zhangziliang@le.com','zhouliangyue@le.com','yangyan1@le.com','liuya1@le.com','qushihui@le.com','chenzhen3@le.com','yangjinhu@le.com','lixiang1@le.com']
            jenkinsServer = "http://cia.devops.letv.com"
        elif phonemodel == 'TV_8094':
            hw = self.buildModel
            receiver = ['tcauto@le.com','letv_spm_tv@le.com','zhanghongliang1@le.com','Letv_TV_Test@le.com','yanggaochuang@le.com','zhaofang@le.com','calvin.wong@le.com','xiaoying@le.com','tongyonghui@le.com','guochunjing@le.com','letv_sqa@le.com','letv_spm@le.com','qihongbin@le.com','zhangziliang@le.com','zhouliangyue@le.com','yangyan1@le.com','liuya1@le.com','qushihui@le.com','chenzhen3@le.com','yangjinhu@le.com','lixiang1@le.com']
            # receiver = ['ext-danhong_zhang@le.com']
            jenkinsServer = "http://cia.devops.letv.com"
        elif phonemodel == 'X7':
            hw = "DVT3"
            receiver = ['tcauto@le.com','letv_mobile_test@le.com','x7team@le.com','levolumetest@le.com','mobile_test_leader@le.com','jiaofuzu1@le.com','levolumetest@le.com','shixuefeng@le.com','jingyun@le.com','shifengbing@le.com','hongxue@le.com','xiaoying@le.com']
        elif phonemodel == "X2":
            hw = "PVT2"
            receiver = ['tcauto@le.com', 'letv_mobile_test@le.com', 'mobile_sw_8996@le.com', 'rencuilian@le.com',
                        'qiaoke@le.com', 'liuxiaoxiao1@le.com', 'wangjing@eastmobile.cn', 'jiaofuzu1@le.com',
                        'levolumetest@le.com','shixuefeng@le.com','jingyun@le.com','shifengbing@le.com','hongxue@le.com','xiaoying@le.com']
        elif phonemodel == "S2":
            hw = "PVT2"
            receiver = ['tcauto@le.com', 'letv_mobile_test@le.com', 'jiaofuzu1@le.com', 'levolumetest@le.com']
        elif phonemodel == "X10":
            hw = "DVT2"
            receiver = ['tcauto@le.com', 'letv_mobile_test@le.com', 'rencuilian@le.com', 'qiaoke@le.com',
                        'liuxiaoxiao1@le.com', 'wangjing@eastmobile.cn', 'hanyu@le.com', 'yinxi@le.com',
                        'ligang9@le.com', 'tongshuqi@le.com', 'xuxin1@le.com', 'yangshuai1@le.com', 'jiaofuzu1@le.com',
                        'levolumetest@le.com']
        elif phonemodel == "X6":
            hw = "DVT2"
            receiver = ['tcauto@le.com', 'letv_mobile_test@le.com', 'jiaofuzu1@le.com', 'levolumetest@le.com']
        else:
            raise Exception

        report = jenkinsServer + "/job/" + self.rootFolder.split("/")[
            -2] + "/" + self.rootFolder.split("/")[-1] + "/artifact/" + self.rootFolder.split("/")[-1] + "/index.html"
        username = 'tcautobuildsystem'
        password = '@!m12012016'

        msgRoot = MIMEMultipart('related')

        msgRoot['Subject'] = '【测试中心】【AutoEmail】【' + phonemodel + '】'+ testType + '自动化测试: ' + version
        msgRoot['To'] = ';'.join(receiver)


        # mailbuglist = []
        # for bugid in self.bugidlist:
        #     issue, summary, status, assignee, resolution = self.getIssueStatus(bugid)
        #     mailbuglist.append(issue, summary, status, assignee, resolution)
        global bugrelist
        bugrelist=[]
        mailbuglist = []
        self.bugidlist = self.bugidlist + self.funcbuglist
        bugrelist=list(set(self.bugidlist))
        for bugid in bugrelist:
            issue,summary,status,assignee,resolution = self.getIssueStatus(bugid)
            mailbuglist.append(bug(issue,summary,status,assignee,resolution))

        totallynum = str(os.popen(
            "grep 'All EXECUTE CASE' " + self.rootFolder + "/index.html | cut -d '(' -f3 | cut -d ')' -f1").read()).strip()
        passrate = str(os.popen(
            "grep -A2 '>Case Pass Rate' " + self.rootFolder + "/index.html | cut -d '=' -f3 | cut -d '<' -f1").read()).strip()
        rebootrnum = str(os.popen(
            "grep -A1 'Total Reboot' " + self.rootFolder + "/index.html | cut -d '>' -f3 | cut -d '<' -f1").read()).split(
            "Reboot")[1].strip()

        tombstonenum = str(os.popen(
            "grep -A1 'Total Tombstone' " + self.rootFolder + "/index.html | cut -d '>' -f3 | cut -d '<' -f1").read()).split(
            "Tombstone")[1].strip()
        fcnum = str(os.popen(
            "grep -A1 'Total Force Close' " + self.rootFolder + "/index.html | cut -d '>' -f3 | cut -d '<' -f1").read()).split(
            "Close")[1].strip()
        anrnum = str(os.popen(
            "grep -A1 'Total ANR' " + self.rootFolder + "/index.html | cut -d '>' -f3 | cut -d '<' -f1").read()).split(
            "ANR")[1].strip()
        Functionnum = len(self.funcbuglist)
        print tombstonenum
        print fcnum
        print anrnum
        print Functionnum
        print passrate
        print totallynum
        param = {}
        param['version'] = version
        param['versionpath'] = self.versionpath
        param['report'] = report

        # bug1 = bug('RUBY-16892','【X2_Auto:smoke:相机】 com.android.camera2发生FC','RESOLVED','姜 天宇','Fixed')
        # bug2 = bug('XIII-16552','[X3_012S][MTBF_India] Launch app music, play music and stop play music,the phone occurred FC:com.google.android.googlequicksearchbox:search','TRACK','管 小鹏','Fixed')

        param['buglist'] = mailbuglist
        param['totallynum'] = totallynum
        param['passrate'] = passrate
        param['title'] = phonemodel + '_Smoke Test Report'
        param['date'] = nowtime
        param['tester'] = config.testerName
        param['hw'] = hw
        param['sw'] = version
        param['anrnum'] = anrnum
        param['fcnum'] = fcnum
        param['rebootrnum'] = rebootrnum
        param['tombstonenum'] = tombstonenum
        param['Functionnum'] = Functionnum

        t = get_template("mail.html")
        c = template.Context(param)
        # print t.render(c)
        msg = MIMEText(t.render(c), 'html', 'utf-8')
        msgRoot.attach(msg)

        msgText = MIMEText(open(self.rootFolder + '/index.html', 'rb').read(), 'base64', 'utf-8')
        msgText['Content-Type'] = 'application/octet-stream'
        msgText['Content-Disposition'] = 'attachment; filename="index.html"'
        msgRoot.attach(msgText)

        smtp = smtplib.SMTP()
        try:
            smtp.connect('smtp.letv.cn')
            smtp.login(username, password)
            smtp.sendmail(sender, receiver, msgRoot.as_string())
        except:
            print 'failed to login to smtp server'

        smtp.quit()

