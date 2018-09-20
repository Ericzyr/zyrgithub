#! /usr/bin/env python
# -*- coding: utf-8 -*-
class C(object):
    a = 'abc'

    def __getattribute__(self, *args, **kwargs):
        print("__getattribute__() is called")
        print args
        return object.__getattribute__(self, *args, **kwargs)

    #        return "haha"
    def __getattr__(self, name):
        print("__getattr__() is called ")
        return name + " from getattr"

    def __get__(self, instance, owner):
        print("__get__() is called", instance, owner)
        return self

    def __getitem__(self, item):
        print ("__getitem__ is called")

    def foo(self, x):
        print(x)


class C2(object):
    d = C()


def getFolderList(path, recursive=False):
    pList = []
    for f in os.listdir(path):
        if os.path.isdir(os.path.join(path, f)):
            pList.append(os.path.join(path, f))
    if recursive:
        for p in pList:
            pList.extend(getFolderList(p,True))
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
                pList.extend(getFileList(os.path.join(path, f),True))
    pList.sort(key=lambda x: os.stat(x).st_ctime)
    return pList


def findMatchFolders(root, pattern, recursive=True):
    """
    找出root目录下所有以name结尾的目录,返回包含所有符合要求的目录路径列表,若为空,返回None
    """

    fl = getFolderList(root, recursive)

    allf = []
    for f in fl:
        if re.match(pattern, str(f).split('/')[-1]):
            allf.append(f)
    allf.sort(key=lambda x: len(x))
    return allf


def forSortKey(x):
    a = re.findall("\d{1,3}", re.sub(root, "", x))
    count = len(a)-1
    value = 0
    for index,i in enumerate(a):
        value += (int(i)+1) * math.pow(100,count-index)
    print value
    return value
#
# def forSortCmp(x, y):
#
#     xa = re.findall("\d{1,3}", re.sub(root, "", x))
#     if str(x).endswith("logcat.log"):
#         xa.append(0)
#     xcount = len(xa) - 1
#     xvalue = 0
#     for index, i in enumerate(xa):
#         xvalue += (int(i) + 1) * math.pow(100, xcount - index)
#
#
#     ya = re.findall("\d{1,3}", re.sub(root, "", y))
#     if str(y).endswith("logcat.log"):
#         ya.append(0)
#     ycount = len(ya) - 1
#     yvalue = 0
#     for index, i in enumerate(ya):
#         yvalue += (int(i) + 1) * math.pow(100, ycount - index)
#
#     if xcount > ycount:
#         return 1
#     elif xcount < ycount:
#         return -1
#     if xvalue > yvalue:
#         return 1
#     elif xvalue < yvalue:
#         return -1
#     return 0

def findMatchFiles(root, pattern, recursive=True):
    """
    找出root目录下所有以name结尾的目录,返回包含所有符合要求的目录路径列表,若为空,返回None
    """

    allf = []
    fil = getFileList(root, recursive)
    for f in fil:
        if re.match(pattern, str(f).split('/')[-1]):
            allf.append(f)
    # allf.sort(key=lambda x: long(''.join(re.findall("\d{1,3}", x))))
    # allf.sort(key=lambda x: ''.join(re.findall("\d{1,3}", re.sub(root,"",x))))
    # allf.sort(key=forSortKey)
    def forSortCmp(x, y):

        xa = re.findall("\d{1,3}", re.sub(root, "", x))
        if str(x).endswith(pattern):
            xa.append(0)
        xcount = len(xa) - 1
        xvalue = 0
        for index, i in enumerate(xa):
            xvalue += (int(i) + 1) * math.pow(100, xcount - index)

        ya = re.findall("\d{1,3}", re.sub(root, "", y))
        if str(y).endswith(pattern):
            ya.append(0)
        ycount = len(ya) - 1
        yvalue = 0
        for index, i in enumerate(ya):
            yvalue += (int(i) + 1) * math.pow(100, ycount - index)

        if xcount > ycount:
            return 1
        elif xcount < ycount:
            return -1
        if xvalue > yvalue:
            return 1
        elif xvalue < yvalue:
            return -1
        return 0

    allf.sort(cmp=forSortCmp)
    # allf.sort(key=lambda x: os.stat(x).st_ctime)
    return allf


def getLogAndParseLog_logcat():
    from error import FC, ANR, Tombstone
    import device
    from fileparser import getLogInfoFromLogcat
    a = device.TV_938()

    b = getLogInfoFromLogcat(a, 'anr',
                             '/home/letv/TV_MTBF/938/938_HK_52S_1230_0104/TV2/LOOP8/testLocalVideo_20170105_181911')
    f = ANR(b, None)
    print f.time
    # print f.brieflog
    print f.maxCpuRate
    print f.maxCpuProcess


def getLogAndParseLog_dropbox():
    from error import FC, ANR, Tombstone
    from fileparser import getLogInfoFromDropbox
    import device
    a = device.TV_938()
    b = getLogInfoFromDropbox('anr', '/home/letv/Desktop/logcatsourcecode/anr')
    print b.log
    f = ANR(b, None)
    print f.time
    # print f.brieflog
    print f.maxCpuRate
    print f.maxCpuProcess
    print f.reason


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

        for index,folder in enumerate(devices[key]):
            try:
                logfile = open(os.path.join(folder, 'case.log'), "r")
                lines = logfile.readlines()
            except IOError:
                lines = ""

            done = False
            for line in lines:
                if line.find(rebootkeyword) != -1:
                    errorhappend.append(FailInfo(folder, "reboot", index+1))
                    done = True
                    break
            if done: continue

            for line in lines:
                if line.find(fckeyword) != -1:
                    errorhappend.append(FailInfo(folder, "fc", index+1))
                    break
                elif line.find(tombstonekeyword) != -1:
                    errorhappend.append(FailInfo(folder, "tombstone", index+1))
                    break
                elif line.find(anrkeyword) != -1:
                    errorhappend.append(FailInfo(folder, "anr", index+1))
                    break
    return errorhappend


class FailInfo:
    def __init__(self, path, type, index=-1):
        self.path = path
        self.type = type
        self.index = index

    def __str__(self):
        return str(self.index) + ' ' + self.type + ' ' + self.path


if __name__ == '__main__':
    import os, re
    import math
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    # getLogAndParseLog_logcat()
    # root = "/home/letv/桌面/MTBF/MTBF_ENV/MTBF_Results/ZL0_CN_20S_01/phone3/LOOP4/testLeGame_20170108_131818"

    # for i in findMatchFiles(root, 'logcat.log', True):
    #     print i
    # from fileparser import getLogInfoFromTrace,getLogInfoFromDropbox,getLogInfoFromLogcat
    # print getLogInfoFromTrace("tombstone",root)
    # print getLogInfoFromDropbox('tombstone',root)

    # from fileparser import getPhoneInfo
    # a = getPhoneInfo("/Users/halu/Desktop/")
    #
    # print a.getJiraVersion()

    # from fileparser import getPhoneInfo
    # from device import TV,Phone,TV_938,Device
    # a = getPhoneInfo("/home/letv/TV_MTBF/938/938_HK_52S_1230_0104/")
    # print a.getJiraVersion()
    # print a.getProjectName()
    # print a.getJiraProjectKey()
    # print a.getJiraShareProjectKey()
    l = getAllFailedCasesPath('/home/letv/TV_MTBF/918_TV/918_HK_56S_0413_0413', rebootkeyword="===Reboot occurred===",
        fckeyword="===FC occurred===", anrkeyword="===ANR occurred===", tombstonekeyword="===Tombstone occurred===")
    for i in l:
        print i
    print len(l)

    # from fileparser import filterMatchLines
    #
    # lines = filterMatchLines(
    #     "//home/letv/TV_MTBF/938_TV/938_reproducebug_1/X4-43_TV4/LOOP2/testPlayMusic_20170528_074500/logcat.log",
    #     'AndroidRuntime', 'E')
    # for i in lines:
    #     print  i









