#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, re
from device import getDevice
import gzip
import sys



def getFolderList(path, recursive=False):
    pList = []
    for f in os.listdir(path):
        if os.path.isdir(os.path.join(path, f)):
            pList.append(os.path.join(path, f))
    if recursive:
        for p in pList:
            pList.extend(getFolderList(p))
    pList.sort(key=lambda x: os.stat(x).st_ctime)
    return pList


def getFileList(path, recursive=False):
    pList = []
    for f in os.listdir(path):
        if not os.path.isdir(os.path.join(path, f)):
            pList.append(os.path.join(path, f))
    if recursive:
        for f in os.listdir(path):
            if os.path.isdir(os.path.join(path, f)):
                pList.extend(getFileList(os.path.join(path, f)))
    # pList.sort(key=lambda x: os.stat(x).st_ctime)
    pList.sort()
    return pList


def findMatchFolders(absolutePath, folderName, recursive=True):
    """
    找出absolutePath目录下包括子文件夹下的所有以folderName结尾的目录,返回包含所有符合要求的目录路径列表,若为空,返回None
    """

    folderNameList = getFolderList(absolutePath, recursive)
    allMatchFolderList = []
    for forderName in folderNameList:
        if re.match(folderName, str(forderName).split('/')[-1]):
            allMatchFolderList.append(forderName)
    allMatchFolderList.sort(key=lambda x: len(x))
    return allMatchFolderList


def findMatchFiles(root, pattern, recursive=True):
    """
    找出root目录下所有以name结尾的目录,返回包含所有符合要求的目录路径列表,若为空,返回None
    """

    allf = []
    fil = getFileList(root, recursive)
    for f in fil:
        if re.match(pattern, str(f).split('/')[-1]):
            allf.append(f)
    allf.sort(key=lambda x: len(x))
    return allf


def getPhoneInfo(path):

    path = os.path.join(path, 'jiraInfo.txt')
    print path
    prop = {}
    try:
        phoneInfo = open(path)
        lines = phoneInfo.readlines()
    except IOError:
        raise Exception("打开jiraInfo文件失败")
        lines = ""

    for line in lines:
        if line.find("==") != -1:
            tmp = line.split('==')
            prop[tmp[0]] = tmp[1].strip()
    try:
        # projectName = prop['buildModel']
        puductName = prop['buildProduct']
    except KeyError:
        raise Exception("jiraInfo中至少需要有buildProduct字段")
    return getDevice(puductName, prop)


def getCaseInfo(caseFolder):
    """get the case step and case class"""


    stepindex = 0
    #################################################
    try:
        logfile = open(os.path.join(caseFolder, 'case.log'), "r")
        lines = logfile.readlines()
    except IOError:
        lines = ""

    step = []
    clazz = title = ''
    for line in lines:
        reboottype=""
        if line.find("INSTRUMENTATION_STATUS: class=") != -1 and line.find("#") != -1:  # get case class
            index = len("INSTRUMENTATION_STATUS: class=")
            clazz = line[index:].rstrip()
        if line.find("INSTRUMENTATION_STATUS: title=") != -1:  # get case class
            index = len("INSTRUMENTATION_STATUS: title=")
            title = line[index:].rstrip()
        elif line.find("INSTRUMENTATION_STATUS: caseStep=") != -1:  # get case step
            stepindex += 1
            line = re.sub(r'INSTRUMENTATION_STATUS: caseStep=\d?\d?\.?', str(stepindex) + '.', line, 1).rstrip()
            step.append(line)
        if line.find("This is UI reboot") != -1:  # get reboot type
            reboottype="This is UI reboot"
        if line.find("This is System reboot") != -1:  # get reboot type
            reboottype="This is System reboot"
    # if len(step) > 20:
    #     step = step[:20]
    #     step.append('...')
    step = '\n'.join(step)

    return CaseInfo(clazz, step,title,reboottype)


class Info:
    def __init__(self,prop):
        self.__dict__.update(prop)

class CaseInfo:
    def __init__(self, clazz, step,title,reboottype):
        self.clazz = clazz
        self.step = step
        self.title = title
        self.reboottype =reboottype


def getAllFailedCasesPath(resultFolder, rebootkeyword="===Reboot happened===", fckeyword="===FC happened===",
                          anrkeyword="===ANR happened===", tombstonekeyword="===Tombstone happened==="):
    devices = {}
    for device in getFolderList(resultFolder):
        tmp = []
        for loop in getFolderList(device):
            for folder in getFolderList(loop):
                tmp.append(folder)
                devices[device.split('/')[-1]] = tmp

    errorhappend = []
    for key in devices.keys():

        for index, folder in enumerate(devices[key]):
            try:
                logfile = open(os.path.join(folder, 'case.log'), "r")
                lines = logfile.readlines()
            except IOError:
                lines = ""

            done = False
            for line in lines:
                if line.find(rebootkeyword) != -1:
                    errorhappend.append(FailInfo(folder, "reboot", index + 1))
                    done = True
                    break
            if done: continue

            for line in lines:
                if line.find(fckeyword) != -1:
                    errorhappend.append(FailInfo(folder, "fc", index + 1))
                    break
                elif line.find(anrkeyword) != -1:
                    errorhappend.append(FailInfo(folder, "anr", index + 1))
                    break
                elif line.find(tombstonekeyword) != -1:
                    errorhappend.append(FailInfo(folder, "tombstone", index + 1))
                    break

    return errorhappend


class FailInfo:
    def __init__(self, path, type, index=-1):
        self.path = path
        self.type = type
        self.index = index

    def __str__(self):
        return str(self.index) + ' ' + self.type + ' ' + self.path


def getLogInfo(bugtype, path, device):

    if bugtype != 'fc' and bugtype != 'anr' and bugtype != 'tombstone':
        raise Exception("无法获取" + bugtype + "类型的log信息")
    # loginfo = getLogInfoFromLogcat(device, bugtype, path)
    # if loginfo is not None:
    #     return loginfo

    loginfo = getLogInfoFromDropbox(bugtype, path)
    if loginfo is not None:
        return loginfo

    if bugtype == 'tombstone':
        loginfo = getLogInfoFromTrace(bugtype, path)
    if loginfo is not None:
        return loginfo
    else:
        return None


def getLogInfoFromDropbox(bugtype, path, foldername='dropbox'):
    """get data form dropbox"""
    if bugtype == 'fc':
        pattern = "app_crash@"
    elif bugtype == 'anr':
        pattern = "app_anr@"
    elif bugtype == 'tombstone':
        pattern = "TOMBSTONE@|native_crash@"

    # 查找dropbox文件夹，无视结构目录
    folders = findMatchFolders(path, foldername, True)
    for folder in folders:
        filename = ''
        files = getFileList(folder)
        for f in files:
            if re.search(pattern,f) and os.path.getsize(f) != 0:
                filename = f.strip()
                break

        # 没有相应的dropbox文件
        if filename == '':
            continue

        try:
            if not filename.endswith('gz'):
                filecontent = open(filename, "r").read()
            else:
                filecontent = gzip.open(filename, 'r').read()
        except IOError, e:
            # 读取文件失败
            print e
            return None

        if bugtype == 'fc':
            log = filecontent
        elif bugtype == 'anr':
            log = '\n\n'.join(filecontent.split('\n\n')[:2])
        elif bugtype == 'tombstone':
            log = '\n\n'.join(filecontent.split('\n\n')[1:3])
        return LogInfo(log, 'dropbox', filename)

    return None


def getLogInfoFromLogcat(device, bugtype, path, filename='logcat.log'):
    """get log,occurTime,logtype"""
    file_path=os.path.join(path, filename)
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        return None

    tag, priority = device.getErrorTagAndPriority(bugtype)
    lines = filterMatchLines(file_path, tag, priority)
    lines = findFirstErrorMsg(lines, bugtype)
    if not lines:
        return None
    flag = ''
    if bugtype == 'tombstone':
        flag = 'Build fingerprint: '
    elif bugtype == 'fc':
        flag = 'FATAL EXCEPTION: '
    elif bugtype == 'anr':
        flag = 'ANR in '

    success = False
    for line in lines:
        if re.search(flag, line):
            success = True
            break
    if not success:
        print "There is no error information in logcat"
        return None

    return LogInfo(''.join(lines), 'logcat')


def getLogInfoFromTrace(bugtype, path):
    """get log,occurTime,logtype"""
    bugtype = bugtype.lower()

    filename = ''
    if bugtype == 'anr':
        folders = findMatchFolders(path, "anr", True)
        for folder in folders:
            files = getFileList(folder)
            for f in files:
                if re.search(r'traces_?\d{0,2}.txt', f) and os.path.getsize(f) != 0:
                    filename = f.strip()
                    break

    elif bugtype == 'tombstone':
        folders = findMatchFolders(path, "tombstone", True)
        for folder in folders:
            files = getFileList(folder)
            for f in files:
                if re.search(r'tombstone_?\d{0,2}', f) and os.path.getsize(f) != 0:
                    filename = f.strip()
                    break

    else:
        raise Exception(bugtype + "类型的bug,没有trace文件")

    # 没有符合的文件
    if filename == '':
        return None

    try:
        logfile = open(filename, "r")
        content = logfile.read()
    except IOError, e:
        # 读取文件失败
        print e
        return None

    if bugtype == 'anr':
        log = content.split('\n\n')[:2]
    else:
        log = content.split('\n\n')[:2]

    return LogInfo('\n\n'.join(log), 'trace')


class LogInfo:
    def __init__(self, log, type, filename=None):
        self.type = type
        self.filename = filename
        self.log = log

    def __str__(self):
        return 'type : ' + self.type + '\n' + 'log : ' + self.log


def isEco(device, error):

    from error import Reboot
    if isinstance(error, Reboot):
        return False
    pkg = error.processname
    file = os.path.join(sys.path[0], device.getComponentConfFileName(True))

    for line in open(file).readlines():

        if line.strip() == '': continue
        if pkg == line.strip().split(",")[0]:
            return True
    return False


def getComponentsFromConfigurationFile(device, iseco):
    pkgToComponentMap = {}
    file = os.path.join(sys.path[0], device.getComponentConfFileName(iseco))

    for line in open(file).readlines():
        line = line.strip()
        componentKeyAndValues = line.split(",")
        key = componentKeyAndValues[0]
        values = componentKeyAndValues[1:]
        pkgToComponentMap.update({key: values})

    return pkgToComponentMap


def getCreateApp(path, pkg, device):
    if pkg == "":
        raise Exception("包名不能为空")
    appnamemap = getComponentsFromConfigurationFile(device, True)
    values = appnamemap[pkg]
    appname = values[1]

    try:
        logfile = open(os.path.join(path, "jiraInfo.txt"), "r")
        lines = logfile.readlines()
    except IOError:
        raise Exception('''没有appinfo文件,请运行:
adb -s ${IPADDRESS} shell dumpsys package |grep -e "Package \[" -e "versionName" | sed 'N;s/\s*\\n\s*/ /' > '''
                        + path + '''/appinfo.txt\n来得到appinfo文件''')
        lines = ""

    for line in lines:
        if line.find(pkg) != -1:
            versionId = line.split("versionName=")[1].strip()
            break
    createApp = appname + '_' + versionId
    return createApp


def getCreateROM(buildVersion):
    createROM = buildVersion.split('_')[0] + '_dailybuild_' + buildVersion.split('_')[1]
    return createROM


def enum(**enums):
    """
    模拟泛型,网上查的,其实我没看懂
    """
    return type('Enum', (), enums)


Format = enum(TAG='TAG', PROCESS='PROCESS', THREAD='THREAD', RAW='RAW', COLOR='COLOR',
              TIME='TIME', THREADTIME='THREADTIME', LONG='LONG', BRIEF='BRIEF', USEC='USEC')


def filterMatchLines(path, tag, priority):
    """
             tag可能包含任意字符,eg.:LogUtils-/PushReceiver.onReceive(Unknown Source)
        """
    l = []
    format = getLogcatOutputFormatOfFile(path)
    f = open(path, "r")

    if format == Format.THREADTIME or format == Format.USEC or format == Format.COLOR:
        mark = priority + ' ' + tag
    elif format == Format.TIME or format == Format.BRIEF or format == Format.TAG:
        mark = priority + '/' + tag
    elif format == Format.PROCESS:
        mark = '^' + priority + '.*' + tag + '\)$'

    for line in f.readlines():
        if re.search(mark, line.strip()):
            l.append(line)
    return l


def findFirstErrorMsg(lines, bugtype):
    bugtype = str(bugtype).lower()
    if bugtype == 'tombstone':
        flag = 'Build fingerprint: '
    elif bugtype == 'fc':
        flag = 'FATAL EXCEPTION: '
    elif bugtype == 'anr':
        flag = 'ANR in '

    success = False
    for index, line in enumerate(lines):
        if success is True and re.search(flag, line):
            lines = lines[:index]
            break
        if success is False and re.search(flag, line):
            success = True
    if not success:
        raise Exception('Format of log is wrong')
    return lines


"""
    switch (p_format->format) {
        case FORMAT_TAG:
                "%c/%-8s: ", priChar, entry->tag);

            I/ActivityManager: Process com.letv.android.supermanager (pid 3891) has died

        case FORMAT_PROCESS:
                "  (%s)\n", entry->tag);
                "%c(%5d) ", priChar, entry->pid);

            I( 1433) Process com.letv.android.supermanager (pid 3891) has died  (ActivityManager)

        case FORMAT_THREAD:
                "%c(%5d:%5d) ", priChar, entry->pid, entry->tid);

            I( 1433: 1470) Process com.letv.android.supermanager (pid 3891) has died

        case FORMAT_RAW:

            Process com.letv.android.supermanager (pid 3891) has died

        case FORMAT_TIME:
                "%s %c/%-8s(%5d): ", timeBuf, priChar, entry->tag, entry->pid);

            02-06 14:47:58.361 I/ActivityManager( 1433): Process com.letv.android.supermanager (pid 3891) has died

        case FORMAT_THREADTIME:
                "%s %5d %5d %c %-8s: ", timeBuf,
                entry->pid, entry->tid, priChar, entry->tag);

            02-06 14:47:58.361  1433  1470 I ActivityManager: Process com.letv.android.supermanager (pid 3891) has died

        case FORMAT_LONG:
                "[ %s %5d:%5d %c/%-8s ]\n",
                timeBuf, entry->pid, entry->tid, priChar, entry->tag);

            [ 02-06 14:47:58.361  1433: 1470 I/ActivityManager ]
            Process com.letv.android.supermanager (pid 3891) has died


        case FORMAT_BRIEF:
        default:
                "%c/%-8s(%5d): ", priChar, entry->tag, entry->pid);

            I/ActivityManager( 1433): Process com.letv.android.supermanager (pid 3891) has died

    }

    %5d(tid/pid)->  [ ]{0,4}\d{1,5}
    %c(priority)->  [VDIWEF]
    %s(time)    ->  \d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}
    %-8s(tag)   ->  [a-zA-Z0-9]{1,}[ ]{0,7}
"""

nanotime = '\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6}'
time = '\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}'
# tag = '[a-zA-Z0-9]{1,}[ ]{0,7}'
tag = '.{1,}?[ ]{0,7}'
pid_tid = '[ ]{0,4}\d{1,5}'
priority = '[VDIWEF]'

Pattern = enum(TAG=priority + '/' + tag + ': ',
               PROCESS=priority + '\(' + pid_tid + '\) ',
               THREAD=priority + '\(' + pid_tid + ':' + pid_tid + '\) ',
               TIME=time + ' ' + priority + '/' + tag + '\(' + pid_tid + '\): ',
               THREADTIME=time + ' ' + pid_tid + ' ' + pid_tid + ' ' + priority + ' ' + tag + ': ',
               LONG='\[ ' + time + ' ' + pid_tid + ':' + pid_tid,
               BRIEF=priority + '/' + tag + '\(' + pid_tid + '\): ',
               USEC=nanotime + ' ' + pid_tid + ' ' + pid_tid + ' ' + priority + ' ' + tag + ': ')


def getLogcatOutputFormatOfContent(content):
    lines = content.split('\n')
    return getFormatOfLine(lines[0])


def getLogcatOutputFormatOfFile(path):

    f = open(path,'r')
    line = ''
    while True:
        line = f.readline()
        if re.search(r'^--------- beginning of ', line):
            continue
        else:
            break
    if line == '':
        raise Exception('No valid line found.')
    return getFormatOfLine(line)


def getFormatOfLine(line):
    if not line:
        raise Exception('Line cannot be empty.')
    format = None

    if re.match(Pattern.THREADTIME, line):
        format = Format.THREADTIME
    elif re.match(Pattern.TIME, line):
        format = Format.TIME
    elif re.match(Pattern.BRIEF, line):
        format = Format.BRIEF
    elif re.match(Pattern.LONG, line):
        raise Exception("Log print format of logcat should not be 'LONG'")
    elif re.match(Pattern.THREAD, line):
        raise Exception("Log print format of logcat should not be 'THREAD'")
    elif re.match(Pattern.PROCESS, line):
        format = Format.PROCESS
    elif re.match(Pattern.TAG, line):
        format = Format.TAG
    elif re.match(Pattern.USEC, line):
        format = Format.USEC
    elif re.match('\x1B\[', line):
        format = Format.COLOR

    if format is None:
        raise Exception("Can't parse the log print format")
    return format
