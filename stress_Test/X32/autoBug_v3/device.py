#! /usr/bin/env python
# -*- coding: utf-8 -*-
import jiraissue,decorator
from jiratools import findMatchJiraVersion,findMatchJiraVersion_E

def getDevice(deviceModel,prop):
    if deviceModel == 'mangosteen':
        device = TV_938()
    elif deviceModel == 'guava':
        device = TV_928()
    elif deviceModel == 'mstarnapoli'or deviceModel == 'mstarnapoli_4k2k':
        device = TV_918()
    elif deviceModel == 'MAX4_70':
        device = TV_8094()
    elif deviceModel == 'msm8960':
        device = TV_8064()
    elif deviceModel == 'U4':
        device = TV_U4()
    elif deviceModel== 'muskmelon':
        device =TV_938soundbar()
    else:
        raise Exception('Device model not support!')

    device.__dict__ = prop
    return device


class Device(object):

    @decorator.memoize
    def getJiraVersion(self, isEco):
        """
        版本获取方式：
        1、如果jiraInfo.txt中有jiraVersion，并且值不为空，则使用jiraVersion所指定的值
        2、如果方式1不能获取版本，且jiraInfo.txt中有buildId和buildType字段，则根据这两个字段去服务器查找匹配的版本，若找到则使用该值
        3、如果方式1、2不能获取版本，且jiraInfo.txt中有versionPath字段，则根据此字段和一定的规则（看方法详情）来拼出来一个版本（不可靠，
        服务器上可能没有这个版本）
        :return: jira上的版本，不完全可靠
        """
        # todo 稳定版本不确定
        # buildTag = self.buildId[-1]
        # if self.getJiraProjectKey() == 'EUISIX' and buildTag == 'T':
        #     nVerion='dailybuild_'+self.versionPath.split('/')[-2]
        # elif self.getJiraProjectKey()=='EUISIX' and buildTag == 'S':
        #     nVerion=None


        if hasattr(self, 'cb') and self.cb is True:
            if hasattr(self,'__CBRomVersion__'):
                return self.__CBRomVersion__
        if isEco:
            projectKey = self.getJiraShareProjectKey()
        else:
            projectKey = self.getJiraProjectKey()

        if hasattr(self, 'jiraVersion') and self.jiraVersion != "":
            return self.jiraVersion


        # if self.getJiraProjectKey() == 'EUISIX':
        #
        #     ver = findMatchJiraVersion_E(projectKey, nVerion)
        #     # ver = findMatchJiraVersion_E(projectKey, 'dailybuild_20170608')
        #     return ver
        if hasattr(self, 'buildId') and hasattr(self, 'buildType') and self.buildId != '' and self.buildType != '':
            ver = findMatchJiraVersion(projectKey, self.buildId, self.buildType)
            if ver is not None:
                return ver
        if hasattr(self, 'versionPath') and self.versionPath != '':
            return self.buildJiraVersionByRule()

        raise Exception("没有可用的信息来获取Jira上的版本，请在jiraInfo.txt文件中填写" +
                        "jiraVersion字段或者buildId和buildType字段或者versionPath字段." +
                        "或者buildId和buildType字段字段不能匹配到版本")

    def getProjectName(self):
        return self.__class__.__name__

    def getJiraProjectKey(self):
        return self.jiraIssue.__name__

    def getJiraShareProjectKey(self):
        return self.jiraShareProject.__name__

    def __str__(self):
        string=''
        for key,value in dict(self.__dict__).iteritems():
            string += key+": "+value+"\n"
        return string


class TV(Device):
    jiraShareProject = jiraissue.TVSHARE

    def getComponentConfFileName(self, eco):
        if eco:
            return 'tv_eco_pkg_component.csv'
        return 'tv_pkg_component.csv'

    def getErrorTagAndPriority(self, errortype):
        if errortype == "fc":
            return 'AndroidRuntime', 'E'
        elif errortype == "anr":
            return 'ActivityManager', 'E'
        elif errortype == "tombstone":
            return 'DEBUG', '[IFE]'

    # def buildJiraVersionByRule(self):
    #     # S250F_branchus_eui5.8_V2202RCN02C060246B06041T_cibn_userdebug_without
    #     buildId = self.buildId[-1]
    #     if buildId == 'T':
    #         # versionpath='_'.join(self.versionPath.split('_')[1:])
    #         # versionHeader=self.versionPath.split('/')[-1].split('_')[0]
    #         # version=versionHeader.upper()+'_'+versionpath.split('T')[0]+'T_'+'_'.join(versionpath.split('_')[-3:])
    #         version="dailybuild_" + self.versionPath.split('/')[-2]
    #         return version
    #     elif buildId == 'S':
    #         # versionpath='_'.join(self.versionPath.split('_')[1:])
    #         # versionHeader=self.versionPath.split('/')[-1].split('_')[0]
    #         # version=versionHeader.upper()+'_'+versionpath.split('S')[0]+'S_'+'_'.join(versionpath.split('_')[-4:])
    #         return self.buildVersion

# class Phone(Device):
#     jiraShareProject = jiraissue.MOSHARE
#
#     def getComponentConfFileName(self, eco):
#         if eco:
#             return 'phone_eco_pkg_component.csv'
#         return 'phone_pkg_component.csv'
#
#     def getErrorTagAndPriority(self, errortype):
#         if errortype == "fc":
#             return 'AndroidRuntime', 'E'
#         elif errortype == "anr":
#             if self.cpu == 'Qualcomm':
#                 return 'ActivityManager', 'E'
#             else:
#                 return 'ANRManager', 'E'
#         elif errortype == "tombstone":
#             if self.cpu == 'Qualcomm':
#                 return 'DEBUG', 'F'
#             else:
#                 raise Exception()
#
#
# class X2(Phone):
#     __CBRomVersion__ = "z_btp_version_le_x2"
#     jiraIssue = jiraissue.RUBY
#     cpu = 'Qualcomm'
#
#     def buildJiraVersionByRule(self):
#         version = 'X2_full_x820_' + '_'.join(
#             self.versionPath.split("/")[-1].split("_")[2:6] + self.versionPath.split("/")[-1].split("_")[8:11])
#         return version
#
#
# class X6(Phone):
#     jiraIssue = jiraissue.XSIX
#     cpu = 'MTK'
#
#     def buildJiraVersionByRule(self):
#         version='X6_'+'_'.join(self.versionPath.split("/")[-1].split("_")[3:7]+self.versionPath.split("/")[-1].split("_")[9:12])
#         return version
#
#     def getErrorTagAndPriority(self, errortype):
#         if errortype == "fc":
#             return 'AndroidRuntime', 'E'
#         elif errortype == "anr":
#             return 'ANRManager', 'E'
#         elif errortype == "tombstone":
#             return 'AEE/DEBUG', 'F'
#
#
# class X7(Phone):
#     __CBRomVersion__ = "z_btp_version_full_x7"
#     jiraIssue = jiraissue.XSEVEN
#     cpu = 'MTK'
#
#     def buildJiraVersionByRule(self):
#         version = self.versionPath.split("/")[-1]
#         versionmatch = '_'.join(version.split("_")[1:6] + version.split("_")[8:])
#         versionmatch = versionmatch.replace("x7", "X7")
#         return versionmatch
#
#     def getErrorTagAndPriority(self, errortype):
#         if errortype == "fc":
#             return 'AndroidRuntime', 'E'
#         elif errortype == "anr":
#             return 'ANRManager', 'E'
#         elif errortype == "tombstone":
#             return 'AEE/AED', 'I'
#
#
# class S2(Phone):
#     jiraIssue = jiraissue.LAFITE
#     cpu = 'Qualcomm'
#
#     def buildJiraVersionByRule(self):
#         version='S2_'+'_'.join(self.versionPath.split("/")[-1].split("_")[2:6]+self.versionPath.split("/")[-1].split("_")[8:11])
#         return version
#
#
# class ZL1(Phone):
#     jiraIssue = jiraissue.CONNECT
#     cpu = 'Qualcomm'
#
#     def buildJiraVersionByRule(self):
#         version='LE_ZL1_'+'_'.join(self.versionPath.split("/")[-1].split("_")[1:6]+self.versionPath.split("/")[-1].split("_")[8:11])
#         return version



class TV_918(TV):
    jiraIssue = jiraissue.EUISIX

    # def buildJiraVersionByRule(self):
    #     # S250F_branchus_eui5.8_V2202RCN02C060246B06041T_cibn_userdebug_without
    #     buildId = self.buildId[-1]
    #     if buildId == 'T':
    #         # versionpath='_'.join(self.versionPath.split('_')[1:])
    #         # versionHeader=self.versionPath.split('/')[-1].split('_')[0]
    #         # version=versionHeader.upper()+'_'+versionpath.split('T')[0]+'T_'+'_'.join(versionpath.split('_')[-3:])
    #         version="dailybuild_" + self.versionPath.split('/')[-2]
    #         return version
    #     elif buildId == 'S':
    #         # versionpath='_'.join(self.versionPath.split('_')[1:])
    #         # versionHeader=self.versionPath.split('/')[-1].split('_')[0]
    #         # version=versionHeader.upper()+'_'+versionpath.split('S')[0]+'S_'+'_'.join(versionpath.split('_')[-4:])
    #         return self.buildVersion

class TV_928(TV):
    jiraIssue = jiraissue.EUISIX

    # def buildJiraVersionByRule(self):
    #     buildId = self.buildId[-1]
    #     if buildId == 'T':
    #         # versionpath='_'.join(self.versionPath.split('/')[-1].split('_')[1:])
    #         # versionHeader=self.versionPath.split('/')[-1].split('_')[0]
    #         # version=versionHeader.upper()+'_'+versionpath.split('T')[0]+'T_'+'_'.join(versionpath.split('_')[-2:])
    #         version="dailybuild_" + self.versionPath.split('/')[-2]
    #         return version
    #     elif buildId == 'S':
    #         # versionpath='_'.join(self.versionPath.split('/')[-1].split('_')[1:])
    #         # versionHeader=self.versionPath.split('/')[-1].split('_')[0]
    #         # version=versionHeader.upper()+'_'+versionpath.split('S')[0]+'S_'+'_'.join(versionpath.split('_')[-2:])
    #         return version


class TV_938(TV):
    __CBRomVersion__ = "z_btp_version_aosp_mangosteen"
    jiraIssue = jiraissue.EUISIX

    # def buildJiraVersionByRule(self):
    #     buildId = self.buildId[-1]
    #     if buildId == 'T' :
    #         # versionpath='_'.join(self.versionPath.split('/')[-1].split('_')[1:])
    #         # versionHeader=self.versionPath.split('/')[-1].split('_')[0]
    #         # version=versionHeader.upper()+'_'+versionpath.split('T')[0]+'T_'+'_'.join(versionpath.split('_')[-2:])
    #         version="dailybuild_" + self.versionPath.split('/')[-2]
    #         return version
    #     elif buildId == 'S':
    #         # versionpath='_'.join(self.versionPath.split('/')[-1].split('_')[1:])
    #         # versionHeader=self.versionPath.split('/')[-1].split('_')[0]
    #         # version=versionHeader.upper()+'_'+versionpath.split('S')[0]+'S_'+'_'.join(versionpath.split('_')[-2:])
    #         version = None
    #         return version

class TV_938soundbar(TV):
    jiraIssue =jiraissue.EUISIX


class TV_8094(TV):
    jiraIssue = jiraissue.EUISIX

    # def buildJiraVersionByRule(self):
    #     # versionHeader=self.versionPath.split('/')[-1].split('_')[0]
    #     # versionpath='_'.join(self.versionPath.split('/')[-1].split('_')[1:])
    #     # version=versionHeader.upper()+'_'+versionpath.split('T')[0]+'T_'+'_'.join(versionpath.split('_')[-2:])
    #     version = "dailybuild_" + self.versionPath.split('/')[-2]
    #     return version


class TV_8064(TV):
    jiraIssue = jiraissue.EUISIX

    # def buildJiraVersionByRule(self):
    #     # versionpath = '_'.join(self.versionPath.split('/')[-1].split('_')[1:])
    #     # version = 'X60_' + versionpath.split('T')[0] + 'T_' + '_'.join(versionpath.split('_')[-2:])
    #     version = "dailybuild_" + self.versionPath.split('/')[-2]
    #     return version

class TV_EUI6(TV):
    jiraissue = jiraissue.EUISIX

    # def buildJiraVersionByRule(self):
    #     version = "dailybuild_" + self.versionPath.split('/')[-2]
    #     return version


class TV_U4(TV):
    jiraissue = jiraissue.EUISIX

    # def buildJiraVersionByRule(self):
    #     buildId = self.buildId[-1]
    #     if buildId == 'T':
    #         # versionpath = ''.join(self.versionPath.split('/')[-1].split('T')[1])
    #         # version = self.buildVersion.split('_')[0]+'_'+versionpath.split('_')[1]
    #         version = "dailybuild_" + self.versionPath.split('/')[-2]
    #         return version
    #     elif buildId == 'S':
    #         # versionpath = ''.join(self.versionPath.split('/')[-1].split('S')[1])
    #         # version = self.buildVersion.split('_')[0]+'_'+versionpath.split('_')[1]
    #         version=None
    #         return version
