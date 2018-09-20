#! /usr/bin/env python
# -*- coding: utf-8 -*-
import fileparser
import error
import sys
import  xlwt
import json
import jiratools
import decorator
from error import FC,ANR,Tombstone,Reboot
import re


def addtosheet(workbook, name, list):
    sheet = workbook.add_sheet(name)

    sheet.write(0, 0, "Index")
    sheet.write(0, 1, "设备")
    sheet.write(0, 2, "重复")
    sheet.write(0, 3, "进程名")
    sheet.write(0, 4, "简要log")
    sheet.write(0, 5, "统计")
    sheet.write(0, 6, "路径")
    for i, item in enumerate(list):
        sheet.write(i+1, 0, item.index)
        sheet.write(i+1, 1, item.path.split('/')[-3])
        sheet.write(i+1, 2, item.key)
        sheet.write(i+1, 3, item.processname)
        sheet.write(i+1, 4, item.brieflog)
        sheet.write(i+1, 5, json.dumps(item.tongji))
        sheet.write(i+1, 6, item.path)

def networkChecking(errors):
    """
    与联网获取的bug比较，看是否重复
    """
    import jiratools

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
                break
            print '查重结果： false\n'
        else:
            print '查重最终结果： false\n'
            error.key = ''
    # return errors


@decorator.memoize
def getIssuesFromServer(projectkey):

    issues = jiratools.getMyJira().search_issues(
        'project= "' + projectkey + '" and status != closed and labels = mtbf', maxResults=1)
    issues = jiratools.getMyJira().search_issues(
        'project= "' + projectkey + '" and status != closed and labels = mtbf', maxResults=issues.total)
    print "found issues from server: ", len(issues)
    return issues

def newworkChecking_singleError(error):

    if isinstance(error, Reboot) or isinstance(error, ANR):
        return ''

    selfloglines = error.brieflog.split('\n')
    if len(selfloglines) < 2:
        return ''

    if fileparser.isEco(phone, error):
        netbuglist = getIssuesFromServer(phone.getJiraShareProjectKey())
    else:
        netbuglist = getIssuesFromServer(phone.getJiraProjectKey())

    for netbug in netbuglist:
        # print netbug.key
        description = netbug.fields.description
        if description is None:
            print 'description is null'
            continue
        description = description.encode("utf-8")

        if description.find('\r\n') != -1:
            descriptionlines = description.split('\r\n')
        else:
            descriptionlines = description.split('\n')

        # for index, line in enumerate(descriptionlines):
        #     if line.find(selfloglines[0]) != -1:
        #         if index != len(descriptionlines)-1 and descriptionlines[index + 1].find(selfloglines[1]) != -1:
        #             return netbug.key
        if isinstance(error , FC):
            selfloglines =error.brieflog.split('\n')
            selflogprocessname = error.processname.strip()
            for index ,line in enumerate(descriptionlines):
                if selflogprocessname !=None:
                    if line.find(selflogprocessname) !=-1:
                        if descriptionlines[index+1].find(selfloglines[0]) !=-1:
                            if descriptionlines[index+2].find(selfloglines[1]) !=-1:
                                return  netbug.key
                elif line.find(selfloglines[0]) !=-1:
                    if  descriptionlines[index+1].find(selfloglines[1]) !=-1:
                        return  netbug.key

        elif isinstance(error ,Tombstone):
            selfloglines =error.brieflog.split('\n')
            for index ,line in  enumerate (descriptionlines):
                if line.find(selfloglines[0]) !=-1:
                    if  descriptionlines[index+1].find(selfloglines[1]) !=-1:
                        return  netbug.key
    else:
        return ''

def networkChecking_all(errors):
    """
    与联网获取的bug比较，看是否重复
    """

    for x, error in enumerate(errors):
        print '本地第%d个bug'%(x+1)
        error.key = newworkChecking_singleError(error)

    # return errors


if __name__ == '__main__':
    resultFolder = sys.argv[1]
    print "resultFolder : "+resultFolder

    phone = fileparser.getPhoneInfo(resultFolder)

    failedCasepaths = fileparser.getAllFailedCasesPath(resultFolder, rebootkeyword="===Reboot occurred===",
        fckeyword="===FC occurred===", anrkeyword="===ANR occurred===", tombstonekeyword="===Tombstone occurred===")

    # for i in failedCasepaths:
    #     print 'fail path : '+i.path, " ", i.type ,i.index
    # print "count : ",len(failedCasepaths)

    from fileparser import FailInfo
    # failedCasepaths = [FailInfo('/home/letv/TV_MTBF/918_TV/918_51S_1122_1125/918_S40Air_TV1/LOOP6/testCopyAAAFolder_20161128_141509','tombstone'),
    # failedCasepaths = [FailInfo('/home/letv/TV_MTBF/918_TV/918_51S_1122_1125/918_S40Air_TV1/LOOP21/testDownloadApp_20161130_164606','fc')]

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

    #本地查重
    filteredErrorList = []
    devicemap = {}
    for item in errorList:
        for i, filteredItem in enumerate(filteredErrorList):
            if item.equals(filteredItem):
                devicemap[i].append(item.getDevice())
                break
        else:
            devicemap.update({
                len(filteredErrorList): [item.getDevice(), ]
            })
            filteredErrorList.append(item)

    #统计
    alldevicelist = [i.split('/')[-1] for i in fileparser.getFolderList(resultFolder)]

    for i, filteredItem in enumerate(filteredErrorList):
        # print '-------------------------------------\n'
        # print filteredItem
        alldevicemap = {x: 0 for x in alldevicelist}
        tmplist = devicemap[i]
        for x in tmplist:
            for y in alldevicelist:
                if x == y:
                    alldevicemap[y] += 1
        filteredItem.tongji = alldevicemap

    #     print '\n',alldevicemap,'\n'
    #
    # print 'filtered count : ',len(filteredErrorList)


    # 联网查重
    print ""
    print "======================================================================="
    print "==========================联网查重====================================="
    print "======================================================================="
    print "查重前： ", len(filteredErrorList)

    networkChecking_all(filteredErrorList)
    for i in filteredErrorList:
        print '...'
        print i.key
    print "查重后： ", len(filteredErrorList)


    # networkChecking(filteredErrorList)
    # for  i in filteredErrorList:
    #     print '...'
    #     print i.key
    # print "查重后： ", len(filteredErrorList)


    fc = []
    anr = []
    tombstone = []
    reboot =[]
    for i, filteredItem in enumerate(filteredErrorList):
        if filteredItem.getName().lower()=="fc":
            fc.append(filteredItem)
        elif filteredItem.getName().lower()=="anr":
            anr.append(filteredItem)
        elif filteredItem.getName().lower()=="tombstone":
            tombstone.append(filteredItem)
        elif filteredItem.getName().lower()=="reboot":
            reboot.append(filteredItem)

    w = xlwt.Workbook(encoding = 'utf-8')

    addtosheet(w,'fc',fc)
    addtosheet(w, 'anr', anr)
    addtosheet(w, 'tombstone', tombstone)
    addtosheet(w, 'reboot', reboot)

    import time
    nowtime=time.strftime('%Y-%m-%d',time.localtime(time.time()))

    w.save('file'+nowtime+".xls")


