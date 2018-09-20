#! /usr/bin/env python
# -*- coding: utf-8 -*-
import fileparser
import error
import converter
import jiratools
import jiraissue
from jira import JIRAError
from device import Phone,TV
import os

import sys
reload(sys)
sys.setdefaultencoding('utf8')


def customRules(issue):

    fields = issue.fields
    # 如果是CB，加cb标签，便于以后在jira中搜索
    if cb:
        fields['labels'].append('cb')
    # 组件为空时，使用我们定义的组件名，然后分配人更改为自己
    if fields['components'][0]['name'] == "Auto_Report_TC_Auto":
        import config
        fields['assignee'] = {'name': config.user}
    issue.fields = fields
    return issue


def error2issue(error, phone, converter):
    # todo createApp/createROM都放在phone里,创建所有issue的字段就统一了
    isEco = fileparser.isEco(phone, error)
    error.caseInfo = fileparser.getCaseInfo(error.path)
    summary, description, component = converter.convert(error, phone, isEco)
    if isEco:
        if isinstance(phone, Phone):
            createApp = fileparser.getCreateApp(resultFolder, error.processname, phone)
            jiratools.checkVersion(phone.getJiraShareProjectKey(), createApp)
            a = jiraissue.MOSHARE(summary, description, phone.getJiraVersion(True), component, createApp,
                                  phone.getProjectName())
        elif isinstance(phone, TV):
            createApp = fileparser.getCreateApp(resultFolder, error.processname, phone)
            createROM = fileparser.getCreateROM(phone.buildVersion)
            # jiratools.checkVersion(phone.getJiraShareProjectKey(), createApp)
            #jiratools.checkVersion(phone.getJiraShareProjectKey(), createROM)
            a = jiraissue.TVSHARE(summary, description, phone.getJiraVersion(True), component, createApp, createROM)
    else:
        issue = phone.jiraIssue
        a = issue(summary, description, phone.getJiraVersion(False), component, error.time)
    # print 'summary : ' + '\n' + summary + '\n' + \
    #       'component : ' + '\n' + component + '\n' + \
    #       'time : ' + '\n' + error.time + '\n' + \
    #       'romversion : ' + '\n' + phone.jiraVersion + '\n' + \
    #       'description : ' + '\n' + description + '\n\n'
    a = customRules(a)
    a.path = error.path
    a.type = error.getName()
    a.isEco = isEco
    return a


def networkChecking(errors):
    """
    与联网获取的bug比较，看是否重复
    """
    notrepeat = []
    repeat = []
    for x, error in enumerate(errors):
        print '本地第%d个bug'%(x+1)
        if fileparser.isEco(phone, error):
            netbuglist = jiratools.getIssuesFromServer(phone.getJiraShareProjectKey())
        else:
            netbuglist = jiratools.getIssuesFromServer(phone.getJiraProjectKey())

        for netbug in netbuglist:
            print netbug.key
            if error.equals(netbug):
                print '查重结果： true\n'
                error.key = netbug.key
                repeat.append(error)
                break
            print '查重结果： false\n'
        else:
            print '查重最终结果： false\n'
            notrepeat.append(error)
    return notrepeat, repeat


if __name__ == '__main__':
    resultFolder = sys.argv[1]

    try:
        sys.argv[2]
        cb = True
    except IndexError:
        cb = False

    rebootrnum = int(os.popen(
        "grep -A1 'Total Reboot' " + resultFolder + "/index.html | cut -d '>' -f3 | cut -d '<' -f1").read().split(
        "Reboot")[1].strip())
    tombstonenum = int(os.popen(
        "grep -A1 'Total Tombstone' " + resultFolder + "/index.html | cut -d '>' -f3 | cut -d '<' -f1").read().split(
        "Tombstone")[1].strip())
    fcnum = int(os.popen(
        "grep -A1 'Total Force Close' " + resultFolder + "/index.html | cut -d '>' -f3 | cut -d '<' -f1").read().split(
        "Close")[1].strip())
    anrnum = int(os.popen(
        "grep -A1 'Total ANR' " + resultFolder + "/index.html | cut -d '>' -f3 | cut -d '<' -f1").read().split(
        "ANR")[1].strip())
    passrate = str(os.popen(
            "grep -A2 '>Case Pass Rate' " + resultFolder + "/index.html | cut -d '=' -f3 | cut -d '<' -f1").read()).strip()
    if cb and (tombstonenum + fcnum + anrnum + rebootrnum == 0) and float(passrate[:-1]) >= 90:
        print "检测到本次测试是CB测试，且没有bug，因此不发送邮件。"
        exit()

    bugidlist = []

    phone = fileparser.getPhoneInfo(resultFolder)
    phone.cb = cb

    failedCasepaths = fileparser.getAllFailedCasesPath(resultFolder)

    for i in failedCasepaths:
        print 'fail path : '+i.path
    # from fileparser import FailInfo
    # from device import getDevice
    # phone = getDevice("le_x2","","smb://imgrepo-cnbj-mobile.devops.letv.com/dailybuild/ruby/cn/le_x2/daily/20170121/full_x820_ruby_dev_leui_FEXCNFN5950001212D_20170121_021706_whole_netcom_userdebug")
    # failedCasepaths = [FailInfo('/home/letv/桌面/MTBF/MTBF_ENV/MTBF_Results/ZL0_CN_20S_01/phone3/LOOP11/testSendSMSFromCallLog_20170112_150131','fc')]
    #                    FailInfo('/Users/halu/Desktop/540/Phone1/LOOP1/testWifiConnection_20161201_063847_mf_anr','anr')]

    errorList = []
    for item in failedCasepaths:
        if item.type == "reboot":
            logInfo = None
        else:
            logInfo = fileparser.getLogInfo(item.type, item.path, phone)
            if logInfo is None:
                print 'can not get loginfo, so skip this case : ' + item.path
                continue
        bug = error.getError(item, logInfo)
        errorList.append(bug)


    # 本地查重
    print "======================================================================="
    print "==========================本地查重====================================="
    print "======================================================================="
    print "查重前： ", len(errorList)
    filteredErrorList = []
    for x, item in enumerate(errorList):
        for y, filteredItem in enumerate(filteredErrorList):
            print "旧列表中第%d个bug与新列表中第%d个bug对比"%(x,y)
            if item.equals(filteredItem):
                print '查重结果： true\n'
                break
            print '查重结果： false\n'
        else:
            print '查重总结果： false， 将%d放入新列表\n'%x
            filteredErrorList.append(item)
        print '------------------------'
    print "查重后： ", len(filteredErrorList)

    # 联网查重
    print ""
    print "======================================================================="
    print "==========================联网查重====================================="
    print "======================================================================="
    print "查重前： ", len(filteredErrorList)
    notrepeat, repeat = networkChecking(filteredErrorList)
    print "查重后： ", len(notrepeat)

    jiraissueList = []
    # 根据联网查重的结果,添加附件或者准备报bug
    converter = converter.Smoke_Converter()
    for item in repeat:
        jiratools.add_attachment_and_comment(item.path, item.key, phone.versionPath, "autotest")
        bugidlist.append(item.key)
    for item in notrepeat:
        jiraissueList.append(error2issue(item, phone, converter))

    # 检查版本,如果服务器不存在此版本则尝试创建,如果创建失败(没有权限),则阻塞代码继续执行
    hasEco = False
    hasNormal = False
    for field in jiraissueList:
        if field.isEco == True:
            hasEco = True
        else:
            hasNormal = True
    if jiraissueList:
        if hasEco and isinstance(phone,Phone):
            jiratools.checkVersion(phone.getJiraShareProjectKey(), phone.getJiraVersion(True))
        if hasNormal:
            jiratools.checkVersion(phone.getJiraProjectKey(), phone.getJiraVersion(False))

    for i in jiraissueList:
        print i
        print '======================================================================'
    print len(jiraissueList)

    # 报bug
    for i in jiraissueList:
        # try:
        issue = jiratools.getMyJira().create_issue(fields=i.fields)
        # except JIRAError, e:
        #     print e
        #     continue
        print "reported: ", issue
        issue.type = i.type
        bugidlist.append(issue.key)
        jiratools.add_attachment_and_comment(i.path, bugidlist[-1], phone.versionPath, "autotest")

    # 发邮件报告
    from mail import Sendmail
    funcbuglist = []
    # if phone.getProjectName()=='TV_938' and cb == True:
    #     funcbuglist.append('DEMETER-40068')
    # elif phone.getProjectName()=='TV_938':
    #     funcbuglist.append('DEMETER-43671')
    #     # funcbuglist.append('DEMETER-52579')
    # if phone.getProjectName()=='TV_8094':
    #     funcbuglist.append('HERACLES-16337')
    #     funcbuglist.append('HERACLES-16333')
    #     funcbuglist.append('HERACLES-16323')
    #     # bugidlist.append('HERACLES-16445')
    sendmail = Sendmail(resultFolder, phone, bugidlist, funcbuglist, cb)
    sendmail.sendMail()
