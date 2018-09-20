#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import xlrd

import converter
import error
import fileparser
import jiraissue
import jiratools
from fileparser import FailInfo
from device import TV

reload(sys)
sys.setdefaultencoding("utf-8")


def customRules(issue):
    import config
    fields = issue.fields
    # 生态要判断下版本是否需要创建
    if fields['project']['key'] == "MOSHARE":
        jiratools.checkVersions("MOSHARE", fields['customfield_12614'][0]['name'],
                                fields['customfield_12613'][0]['name'])
    # 组件为空时，使用我们定义的组件名，然后分配人更改为自己
    if fields['components'][0]['name'] == "AUTO_Report_TC":
        import config
        fields['assignee'] = {'name': config.user}
    fields['labels'] +=config.labels
    # fields['labels'].append(phone.lables)
    issue.fields = fields
    return issue



def error2issue(error, phone, converter):
    # todo createApp/createROM都放在phone里,创建所有issue的字段就统一了
    isEco = fileparser.isEco(phone, error)
    error.caseInfo = fileparser.getCaseInfo(error.path)
    summary, description, component = converter.convert(error, phone, isEco)

    if isEco:
        if isinstance(phone ,TV):
            createApp = fileparser.getCreateApp(resultFolder, error.processname, phone)
            createROM = fileparser.getCreateROM(phone.jiraVersion)
            # jiratools.checkVersion(phone.getJiraShareProjectKey(), createApp)
            #jiratools.checkVersion(phone.getJiraShareProjectKey(), createROM)
            a = jiraissue.TVSHARE(summary, description, phone.getJiraVersion(True), component, createApp, createROM)
    else:
        issue = phone.jiraIssue
        a = issue(summary, description, phone.getJiraVersion(False), component, phone,testType,testPhase)
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


    #从文件读取数据
    logfile = xlrd.open_workbook("file.xls")
    failedCasePaths = []
    repeat_map = {}
    for i in range(4):
        table = logfile.sheets()[i]
        nrows = table.nrows
        for line in range(1,nrows):
            failedCasePaths.append(FailInfo(table.row_values(line)[6], table.name, table.row_values(line)[0]))
            repeat_map.update({table.row_values(line)[6] : table.row_values(line)[2]})

    resultFolder = '/'.join(failedCasePaths[0].path.split('/')[:-3])
    print resultFolder

    phone = fileparser.getPhoneInfo(resultFolder)


    testType =phone.testType
    testPhase =phone.testPhase

    for i in failedCasePaths:
        print i
    print "count : ", len(failedCasePaths)

    #获取log信息,生成error对象
    errorList = []
    for item in failedCasePaths:
        if item.type == "reboot":
            logInfo = None
        else:
            logInfo = fileparser.getLogInfo(item.type, item.path, phone)
            if logInfo is None:
                print 'can not get loginfo, so skip this case : ' + item.path
                continue
        bug = error.getError(item, logInfo)
        errorList.append(bug)
    print len(errorList)

    for item in errorList:
        if item.path in repeat_map.keys():
            item.key = repeat_map[item.path]


    bugidlist = []

    jiraissueList = []
    # 根据联网查重的结果,添加附件或者准备报bug
    converter = converter.TV_MTBF_Converter()
    for item in errorList:
        if item.key != "":
            jiratools.add_attachment_and_comment(item.path, item.key, phone.versionPath, "TV-MTBF")
            bugidlist.append(item.key)
        else:

            jiraissueList.append(error2issue(item, phone, converter))

    print len(jiraissueList)
    # for i in jiraissueList:
    #     print i
    #     print "+"*35

    #汇报bug并且记录到autobugresult.csv中
    import os
    reported = []
    if os.path.exists(os.path.join(resultFolder,'autobugresult.csv')):
        a = open(os.path.join(resultFolder,'autobugresult.csv'), 'r+')
        for line in a.readlines():
            reported.append(line.split(',')[-1].strip())
    else:
        a = open(os.path.join(resultFolder, 'autobugresult.csv'), 'w')

    for i in jiraissueList:
        if i.path in reported:
            print 'this issue have been reported:',i.path

        issue = jiratools.getMyJira().create_issue(fields=i.fields)
        print "report success: ",issue
        a.write(str(issue.fields.components[0])+','+i.type +','+issue.key+','+str(issue.fields.summary)+','+
                str(issue.fields.status)+','+str(issue.fields.assignee)+','+str(issue.fields.resolution)+','+i.path + '\n')
        jiratools.add_attachment_and_comment(i.path, issue.key, phone.versionPath, "TV-MTBF")



    #
    # import os
    # a = open(os.path.join(resultFolder,'autobugresult.csv'), 'w')
    # for issue in bugidlist:
    #     b = str(issue.fields.components[0])+','+issue.type +','+issue.key+','+str(issue.fields.summary)+','+str(issue.fields.status)+','+str(issue.fields.assignee)+','+str(issue.fields.resolution)
    #     a.write(b)
    #     a.write('\n')







