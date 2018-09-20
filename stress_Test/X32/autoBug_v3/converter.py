#! /usr/bin/env python
# -*- coding: utf-8 -*-
import jiratools
import fileparser
from error import Reboot


class Common:

    def convert(self, error, phone, iseco):
        return self.getSummary(error, phone), self.getDescription(error, phone), self.getComponent(error, phone, iseco)

    def getComponent(self,error, device, iseco):
        if isinstance(error, Reboot):
            return "Auto_Report_TC_Auto"
        pkgToComponentMap = fileparser.getComponentsFromConfigurationFile(device, iseco)
        key = error.processname
        if key == '':
            return "Auto_Report_TC_Auto"
        component = "Auto_Report_TC_Auto"

        if key in pkgToComponentMap:
            mComponents = pkgToComponentMap[key]
            titles = pkgToComponentMap['###']

            if iseco:
                component = mComponents[0]
            else:
                for i in range(len(titles)):
                    if titles[i].lower() == device.getJiraProjectKey().lower():
                        if mComponents[i] == '':
                            component = mComponents[0]
                        else:
                            component = mComponents[i]

        return component


class Smoke_Converter(Common):

    def getDescription(self,error, phone):
        import config
        testPersonName = config.testerName
        testPersonTell = config.testerTell
        testPersonEmail = config.testerEmail

        versionpath = phone.versionPath
        projectname = phone.getProjectName()
        casestep = error.caseInfo.step
        log = error.fulllog
        logtype = error.logtype
        errortype = error.getName()

        # "Hardware version：" + projectname + \
        description = "" + \
                      "[Version]:" + "\n" + \
                      "Test version：" + versionpath.split("/")[-1] + '\n' + \
                      "Version path：" + versionpath + \
                      "\n\n" + \
                      "[Step]:" + '\n' + casestep.rstrip() + \
                      "\n\n" + \
                      "[Actual result]:" + "\n" + \
                      errortype + " happened" + \
                      "\n\n" + \
                      "[Expected result]:" + "\n" + \
                      "No " + errortype + \
                      "\n\n" + \
                      "[Log]: " + logtype + "\n" + "---++---" + '\n' + log + "\n" + "---++---" + "\n" + \
                      "For log details, please see the attachment." + \
                      "\n" + \
                      "\n" + \
                      "\n" + \
                      "If you have questions,please contact: \n" + \
                      "Name：" + testPersonName + "\n" + \
                      "Phone number：" + testPersonTell + "\n" + \
                      "E-mail：" + testPersonEmail
        return description

    def getSummary(self,error, device):
        casenames = error.processname.split('.')[-1].strip()

        summary = "[AUTO][" + device.getProjectName() + ":Smoke:" + casenames + "] " + error.getName() + " occurred in " + error.processname
        return summary


class TV_MTBF_Converter(Common):

    def getComponent(self, error, device, iseco):
        if isinstance(error, Reboot):
            return "Auto_Report_TC_Auto"
        return Common.getComponent(self,error, device, iseco)


    def getDescription(self,error,phone):

        import config
        testPersonName = config.testerName
        testPersonTell = config.testerTell
        testPersonEmail = config.testerEmail
        log = error.fulllog
        logtype = error.logtype
        versionpath = phone.versionPath
        projectname = phone.getProjectName()
        casestep = error.caseInfo.step

        errortype = error.getName()
        description = "【测试版本】：(实际测试版本以下面的路径为准)" + '\n' + \
                      "版本：" + versionpath.split("/")[-1] + '\n' + \
                      "版本路径："+ versionpath + \
                      '\n\n' + \
                      "【操作步骤】" + "\n" + \
                      "MTBF 测试是自动化测试，包含许多应用循环测试（桌面切换，浏览器，下载，图库，乐拍,乐视视频,同步影" \
                      "院,乐搜,下载中心,Live,信号源,乐见桌面,乐视体育等等），其中出问题时在跑下面的case,具体原因还需要开发结合log具体分析。" + '\n' + \
                      casestep.rstrip() + "\n\n" + \
                      "【实际结果】" + '\n' + \
                      errortype + " happened" + \
                      '\n\n' + \
                      "【occurred time】"+"\n"+\
                      "【期待结果】" +"\n"+ \
                      "电视不应该发生" + errortype + \
                      "\n\n" + \
                      "[Log]: " + logtype + "\n" + "---++---" + '\n' + log + "\n" + "---++---" + "\n" + \
                      "有关日志详细信息，请参阅附件." + '\n' + \
                      "【联系方式】" + "\n" + \
                      "姓名：" + testPersonName + "\n" + \
                      "电话：" + testPersonTell + "\n" + \
                      "电子邮箱：" + testPersonEmail

        return description


    def getSummary(self,error,phone):
        summary = "[AUTO][" + phone.getProjectName() + ' ' + phone.buildModel + ":MTBF:] " + error.caseInfo.title + "时发生" + error.getName() +": " + error.processname
        if error.caseInfo.reboottype !=None:
            summary +=error.caseInfo.reboottype
        print summary
        return summary

# print unicode('Settings_UI',"utf-8") in a
# print u'\u9886\u5148\u7248\u6d77\u5916\u901a\u7528\u7248'
# print unicode("领先版海外通用版", "utf-8") in a
