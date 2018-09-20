#! /usr/bin/env python
# -*- coding: utf-8 -*-

from jira import JIRA
import os
import config
import re
import decorator

__url = config.url
__user = config.user
__pwd = config.pwd

__myJira = None

def getMyJira():
    global __myJira
    if __myJira is None:
        __myJira = JIRA(server=__url,basic_auth=(__user,__pwd))
    return __myJira


def findMatchJiraVersion(projectKey = "XSEVEN", buildId = "KGXCNFN5960411181D", buildType = "userdebug"):

    for i in getProjectVersions(projectKey):
        if re.search(buildId, i):
            if re.search(buildType, i):
                return i
    return None


def findMatchJiraVersion_E(projectKey, nVerion):
    for i in getProjectVersions(projectKey):
        if re.search(nVerion, i):
            return i
    return None


@decorator.memoize
def getIssuesFromServer(projectkey):
    bugs = []
    issues = getMyJira().search_issues(
        'project= "' + projectkey + '" and status != closed and labels =auto_report')
    for issue in issues:
        summary = issue.fields.summary.encode("utf-8")
        description = issue.fields.description.encode("utf-8")
        networkbugtype = getBugTypeFromSummary(summary)
        if description.find('---++---') == -1 or networkbugtype == '':
            continue
        networklogtype = description.split('[Log]: ')[1].split('\n')[0].strip()
        tmpdata = description.split('---++---')[1].strip()

        import error
        from fileparser import FailInfo, LogInfo
        bug = error.getError(FailInfo('network', networkbugtype), LogInfo(tmpdata, networklogtype))
        bug.key = issue.key.encode("ascii")
        bugs.append(bug)
    return bugs


def getBugTypeFromSummary(summary):
    tombstoneP = '[Tt][Oo][Mm][Bb][Ss][tT][Oo][nN][Ee]'
    fcP = '[fF][Cc]'
    anrP = '[Aa][nN][rR]'
    if re.search(tombstoneP,summary):
        return 'tombstone'
    elif re.search(fcP,summary):
        return 'fc'
    elif re.search(anrP,summary):
        return 'anr'
    else:
        return ''


def checkVersion(projectkey,version):

    exists = False
    for v in getProjectVersions(projectkey):
        if version == v:
            print 'version: %s exist'%(version)
            exists = True

    if not exists:
        print 'create version: %s'%(version)
        getMyJira().create_version(name=version,project=projectkey)


@decorator.memoize
def getProjectVersions(projectKey):

    versionlist = []
    versions = getMyJira().project_versions(projectKey)
    for version in versions:
        print version
        versionlist.append(version.name.encode("utf-8"))
    return versionlist


def add_attachment_and_comment(path, issue, versionPath, serverSubFolder):
    # 添加log到附件并且添加comments。log小于30M则直接添加附件，大于30M则上传服务器。并且添加相应的备注信息
    logName = path.split(os.sep)[-1]
    print logName
    os.system('cd ' + path + ' && zip -r ' + logName + '.zip ./*')
    logPath = path + '/' + logName + '.zip'

    if os.path.getsize(logPath) < 30000000:
        getMyJira().add_attachment(issue, logPath)
        loglocation = 'Log added to attachment: ' + logName + '.zip'
    else:
        os.system(
            'smbclient //10.148.18.17/jiralog/ -c "cd '+ serverSubFolder +';put ' + logPath + ' ' + logName + '.zip" -N')
        loglocation = 'Log: ' + '\n' + \
                      '//10.148.18.17/jiralog/'+ serverSubFolder +'/' + logName + '.zip'

    comment = 'This bug was happended in this round of testing.' + '\n' + \
              'Version: ' + '\n' + \
              versionPath + '\n' + \
              loglocation
    getMyJira().add_comment(issue, comment)
