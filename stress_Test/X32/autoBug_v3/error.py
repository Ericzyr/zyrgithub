#! /usr/bin/env python
# -*- coding: utf-8 -*-
from abc import abstractmethod
import re
import time
import os
from decorator import memoize
from fileparser import Format, Pattern, getLogcatOutputFormatOfContent

def getError(failInfo,logInfo):

    errorType = failInfo.type.lower()
    if errorType == "fc":
        error = FC(logInfo)
    elif errorType == "anr":
        error = ANR(logInfo)
    elif errorType == "tombstone":
        error = Tombstone(logInfo)
    elif errorType == "reboot":
        error = Reboot()
    else:
        raise Exception("don't support "+errorType + " type")
    error.path = failInfo.path
    error.index = failInfo.index
    return error

class Error(object):

    def __init__(self,logInfo):
        self.logtype = logInfo.type.lower()
        self.processname = ''
        self.parseLog(logInfo)
        # .split(':')[0]--->com.letv.android.letvlive:cde
        self.processname = self.processname.strip().split(':')[0]

    @abstractmethod
    def equals(self, error):
        pass

    def parseLog(self,logInfo):

        self.fulllog = logInfo.log

        if self.logtype == "logcat":
            self.parseLogFromLogcat(logInfo)
        elif self.logtype == "dropbox":
            self.parseLogFromDropbox(logInfo)
        elif self.logtype == "trace":
            self.parseLogFromTrace(logInfo)
        else:
            raise Exception

    def getDevice(self):
        return str(self.path).split('/')[-3]

    def getName(self):
        return self.__class__.__name__

    def __str__(self):
        msg = 'path : ' + self.path + '\n'\
            'bugtype : ' + self.getName() + '\n'\
            'logtype : ' + self.logtype + '\n'\
            'processname : ' + self.processname + '\n'\
            'time : ' + self.time + '\n'
        if self.getName().lower() == "anr" and self.reason != '':
            msg += 'reason : ' + self.reason + '\n'
        msg += 'brieflog : \n' + self.brieflog + '\n'
        return msg


class FC(Error):

    def __init__(self,logInfo):
        super(FC, self).__init__(logInfo)

    def equals(self,obj):
        if not isinstance(obj,FC):
            return False
        if self.processname.strip() != obj.processname.strip():
            return False
        selfloglines = self.brieflog.split('\n')
        objloglines = obj.brieflog.split('\n')
        for i in range(2):
            # print '本地', selfloglines[i]
            # print '远程', objloglines[i]
            # print '---------------------------------'
            if selfloglines[i].strip() != objloglines[i].strip():
                return False
        return True


    def parseLogFromLogcat(self, logInfo):

        loglist = getLogEntryList(self ,logInfo)

        self.time = loglist[0].time

        self.brieflog = []
        for log in loglist:
            if re.search(r'FATAL EXCEPTION: ',log.message):
                continue
            if re.search(r'Process: ',log.message):
                self.processname = str(log).split('Process: ')[1].split(',')[0].strip()
                continue
            self.brieflog.append(log.message)

        self.brieflog = '\n'.join(self.brieflog)

    def parseLogFromDropbox(self,logInfo):
        if logInfo.filename != None:
            self.time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(logInfo.filename.split('@')[1].split('.')[0][:-3])))

        if logInfo.log.find('\r\n') != -1:
            blocks = logInfo.log.split('\r\n\r\n')
        else:
            blocks = logInfo.log.split('\n\n')

        self.brieflog = blocks[1]

        for line in blocks[0].split('\n'):
            if re.search(r'Process: ',line):
                self.processname = str(line).split('Process: ')[1].strip()
                break


class ANR(Error):

    def __init__(self,logInfo):
        self.reason = ''
        super(ANR, self).__init__(logInfo)

    def equals(self,obj):
        # todo 还需优化
        if not isinstance(obj,ANR):
            return False
        if self.maxCpuRate > 70 and obj.maxCpuRate > 70:
            if self.maxCpuProcess == obj.maxCpuProcess:
                return True
        if self.processname != obj.processname:
            return False
        if self.reason != None and obj.reason != None and self.reason != obj.reason:
                return False
        return True

    # def parseLogFromTrace(self,logInfo):
    #     log = logInfo.log.split('\n')
    #     for line in log:
    #         if re.search(r'----- pid',line):
    #             self.time = str(line).split('at')[1].split('------')[0].strip()
    #             continue
    #         if re.search(r'Cmd line: ',line):
    #             self.processname = str(line).split('Cmd line: ')[1].strip()
    #             continue

    def parseLogFromLogcat(self,logInfo):

        loglist = getLogEntryList(self, logInfo)
        
        self.time = loglist[0].time

        for log in loglist:
            if re.search(r'^ANR in ',log.message):
                self.processname = str(log.message).split('ANR in ')[1].split(',')[0]
                if self.processname.find('(') != -1:
                    self.processname = self.processname.split('(')[0]
                break
        for log in loglist:
            if re.search(r'^Reason: ',log.message):
                self.reason = str(log.message).split('Reason: ')[1].split('(')[0].strip()
                break

        for index, log in enumerate(loglist):
            if re.search(r'^CPU usage', log.message):
                self.brieflog = '\n'.join([x.message for x in loglist[index:index+10]])
                nextline = loglist[index+1].message
                tmp = nextline.split()
                self.maxCpuRate = float(tmp[0][:-1])
                self.maxCpuProcess = tmp[1].split('/')[1][:-1]
                break

    def parseLogFromDropbox(self,logInfo):
        if logInfo.filename != None:
            self.time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(logInfo.filename.split('@')[1].split('.')[0][:-3])))

        if logInfo.log.find('\r\n') != -1:
            blocks = logInfo.log.split('\r\n\r\n')
        else:
            blocks = logInfo.log.split('\n\n')

        for line in blocks[0].split('\n'):
            if re.search(r'Process: ', line):
                self.processname = str(line).split('Process: ')[1].strip()
                continue
            if re.search(r'Subject: ', line):
                self.reason = str(line).split('Subject: ')[1].split('(')[0].strip()
                continue
        tmp = blocks[1].split('\n')
        for index, line in enumerate(tmp):
            if re.search(r'^CPU usage', line):
                self.brieflog = '\n'.join(tmp[index:])
                nextline = tmp[index+1]
                tmp = nextline.split()
                self.maxCpuRate = float(tmp[0][:-1])
                self.maxCpuProcess = tmp[1].split('/')[1][:-1]
                break


class Tombstone(Error):

    def __init__(self,logInfo):
        self.brieflog = []
        super(Tombstone, self).__init__(logInfo)
        self.fulllog = self.fulllog.split('stack')[0]

    def equals(self,obj):
        if not isinstance(obj,Tombstone):
            return False
        if self.processname.strip() != obj.processname.strip():
            return False
        selfloglines = self.brieflog.split('\n')
        objloglines = obj.brieflog.split('\n')
        for i in range(2):
            if selfloglines[i].strip() != objloglines[i].strip():
                return False
        return True

    # def parseLogFromTrace(self,logInfo):
    #     blocks = logInfo.log.split('\n\n')
    #
    #     for line in blocks[0].split('\n'):
    #         if re.search(r'pid: ', line):
    #             self.processname = str(line).split('>>> ')[1].split(' <<<')[0]
    #             continue
    #     for line in blocks[1].split('\n'):
    #         if re.search(r'backtrace:', line):
    #             continue
    #         self.brieflog.append(line)
    #     self.brieflog = '\n'.join(self.brieflog)
    #     self.time = 'unknown'

    def parseLogFromLogcat(self,logInfo):

        loglist = getLogEntryList(self, logInfo)
        
        self.time = loglist[0].time

        self.brieflog = []
        for log in loglist:
            if re.search(r'^pid: ', log.message):
                self.processname = str(log.message).split('>>> ')[1].split(' <<<')[0]
                break

        for log in loglist:
            if re.search(r'^#', log.message):
                self.brieflog.append(log.message)
                continue
        self.brieflog = '\n'.join(self.brieflog)

    def parseLogFromDropbox(self,logInfo):
        if logInfo.filename != None:
            self.time = time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.localtime(float(logInfo.filename.split('@')[1].split('.')[0][:-3])))


        if logInfo.log.find('\r\n') != -1:
            blocks = logInfo.log.split('\r\n\r\n')
        else:
            blocks = logInfo.log.split('\n\n')

        for line in blocks[0].split('\n'):
            if re.search(r'pid: ', line):
                self.processname = str(line).split('>>> ')[1].split(' <<<')[0]
                continue
        for line in blocks[1].split('\n'):
            if re.search(r'backtrace:',line):
                continue
            self.brieflog.append(line)
        self.brieflog = '\n'.join(self.brieflog)


class Reboot(Error):

    def __init__(self):
        self.time = 'unknown'
        self.logtype = ''
        self.fulllog = ''
        self.processname = ''
        self.brieflog = ''

    def equals(self,obj):
        return False

    @memoize
    def parseRebootType(self,path):
        try:
            logfile = open(os.path.join(path, 'case.log'), "r")
            lines = logfile.readlines()
        except IOError:
            lines = ""

        for line in lines:
            if line.find("===Kernel Panics===") != -1:
                return "system crash"
        return "systemserver crash"

    def __str__(self):
        msg = 'path : ' + self.path + '\n' \
            'bugtype: ' + self.getName() + '\n' \
            'reboot type : ' + self.parseRebootType() + '\n'
        return msg


def getLogEntryList(bugtype, loginfo):
    """
         tag可能包含任意字符,eg.:LogUtils-/PushReceiver.onReceive(Unknown Source)
    """

    log = loginfo.log
    bugtype = bugtype.__class__.__name__.lower()

    lines = log.split('\n')

    format = getLogcatOutputFormatOfContent(log)
    l = []

    for line in lines:
        if line == '':
            continue
        t = parseLine(line, format)
        l.append(t)
    return l


def parseLine(line, format):
    """
             tag可能包含任意字符,eg.:LogUtils-/PushReceiver.onReceive(Unknown Source)
        """
    if format == Format.THREADTIME or format == Format.COLOR:
        s = """
         case FORMAT_THREADTIME:
                 "%s %5d %5d %c %-8s: ", timeBuf,
                 entry->pid, entry->tid, priChar, entry->tag);

             02-06 14:47:58.361  1433  1470 I ActivityManager: Process com.letv.android.supermanager (pid 3891) has died
        """
        tmplist = re.split('(' + Pattern.THREADTIME + ')', line)

        prefix = tmplist[1]
        message = tmplist[2]

        tmp = prefix.split(' ')
        tmp = deleteEmpty(tmp)

        time = ' '.join(tmp[0:2])
        pid = int(tmp[2])
        tid = int(tmp[3])
        priority = tmp[4]
        tag = ':'.join(' '.join(tmp[5:]).split(':')[:-1])

    elif format == Format.TIME:
        s = """
         case FORMAT_TIME:
                 "%s %c/%-8s(%5d): ", timeBuf, priChar, entry->tag, entry->pid);

             02-06 14:47:58.361 I/ActivityManager( 1433): Process com.letv.android.supermanager (pid 3891) has died
        """
        tmplist = re.split('(' + Pattern.TIME + ')', line)
        prefix = tmplist[1]
        message = tmplist[2]

        tmp = prefix.split(' ')
        tmp = deleteEmpty(tmp)

        time = ' '.join(tmp[0:2])
        pid = int(re.search('\d{1,5}', tmp[-1]).group(0))
        tid = 0
        priority = tmp[2].split('/')[0]
        tag = '('.join('/'.join(' '.join(tmp[2:]).split('/')[1:]).split('(')[:-1])

    elif format == Format.BRIEF:
        s = """
        case FORMAT_BRIEF:
         default:
                 "%c/%-8s(%5d): ", priChar, entry->tag, entry->pid);

             I/ActivityManager( 1433): Process com.letv.android.supermanager (pid 3891) has died
        """
        tmplist = re.split('(' + Pattern.BRIEF + ')', line)

        prefix = tmplist[1]
        message = tmplist[2]

        time = ''
        pid = int(prefix.split('(')[-1].split(')')[0])
        tid = 0
        priority = prefix.split('/')[0]
        tag = '('.join('/'.join(prefix.split('/')[1:]).split('(')[:-1])
    # elif format == Format.THREAD:
    #     s = """
    #     case FORMAT_THREAD:
    #              "%c(%5d:%5d) ", priChar, entry->pid, entry->tid);
    #
    #          I( 1433: 1470) Process com.letv.android.supermanager (pid 3891) has died
    #     """
    #     tmplist = re.split('(' + Pattern.THREAD + ')', line)
    #
    #     prefix = tmplist[1]
    #     message = tmplist[2]
    #
    #     time = ''
    #     pid = int(prefix.split('(')[1].split(':')[0])
    #     tid = int(prefix.split(')')[0].split(':')[1])
    #     priority = prefix.split('(')[0]
    #     tag = ''

    elif format == Format.USEC:
        s = """

        """
        tmplist = re.split('(' + Pattern.USEC + ')', line)

        prefix = tmplist[1]
        message = tmplist[2]

        tmp = prefix.split(' ')
        tmp = deleteEmpty(tmp)

        time = ' '.join(tmp[0:2])
        pid = int(tmp[2])
        tid = int(tmp[3])
        priority = tmp[4]
        tag = ':'.join(' '.join(tmp[5:]).split(':')[:-1])

    elif format == Format.PROCESS:
        s = """
        case FORMAT_PROCESS:
                 "  (%s)\n", entry->tag);
                 "%c(%5d) ", priChar, entry->pid);

             I( 1433) Process com.letv.android.supermanager (pid 3891) has died  (ActivityManager)
        """
        tmplist = re.split('(' + Pattern.PROCESS + ')', line)
        prefix = tmplist[1]
        message = ' '.join(tmplist[2].split()[:-1])

        time = ''
        pid = int(prefix.split('(')[1].split(')')[0])
        tid = 0
        priority = prefix.split('(')[0]
        # 如果tag中包含括号,这里解析出来的tag就是错误的
        tag = tmplist[2].split('(')[-1].split(')')[0]

    elif format == Format.TAG:
        s = """
        case FORMAT_TAG:
                 "%c/%-8s: ", priChar, entry->tag);

             I/ActivityManager: Process com.letv.android.supermanager (pid 3891) has died
        """
        tmplist = re.split('(' + Pattern.TAG + ')', line)

        prefix = tmplist[1]
        message = tmplist[2]

        time = ''
        pid = 0
        tid = 0
        priority = prefix.split('/')[0]
        tag = ':'.join('/'.join(prefix.split('/')[1:]).split(':')[:-1])

    return AndroidLogEntry(time.strip(), priority.strip(), pid, tid, tag.strip(), message.strip(), line.strip())


def deleteEmpty(list):
    while '' in list:
        list.remove('')
    return list


class AndroidLogEntry():

    def __init__(self,time='',priority=0,pid=0,tid=0,tag='',message='',raw=''):
        self.time = time
        self.priority = priority
        self.pid = pid
        self.tid = tid
        self.tag = tag
        self.message = message
        self.raw = raw

    def __str__(self):
        return self.raw
