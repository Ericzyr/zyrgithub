#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from __future__ import division
from django.template import Context
from datetime import datetime
import django
import json
import os
import re
import sys
try:
	from django.template.loader import get_template
except Exception, e:
	print "It appears that Django is not installed. Please install Django"
	print "from the included file Django-1.2.3.tar.gz. The version of "
	print "Django available with your Linux distribution, if you are "
	print "using one, may not be suitable. Unzip and untar the zip "
	print "into any directory, cd into the folder, and, as "
	print "administrator, run:"
	print "python setup.py install"
	sys.exit()

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
reload(sys)
sys.setdefaultencoding('utf-8')


#########################define global variable#####################
LOG_SUFFIX = "/case.log"
LOG_INFO ="/logstack.log"
FLAG_PASS = "OK (1 test)"
######################################################################


class LogParser():
	def __init__(self, planned, folderlist):
# 		print folderlist
		self.resultSheet = []
# 		self.executed = len(folderlist)
		self.executed = 0
		self.summarySheet = {'pass':0, 'plan':planned, 'exed': self.executed, 'tb': 0 , 'anr': 0 , 'fc':0 , 'reset': 0}
		for folder in folderlist:
			self.resultSheet.append(self.parse_log(folder))
		
	def parse_log(self, folder):
		# current case properties
		resultdata = {}
		casechname = ""	
		caseclass = ""
		casename = ""
		exetime = ""
		failreason = ""
		casestep = ""
		ispass = "fail"
		screencap = ""
		logtrack = ""
		anrCount = ""
		fcCount = ""
		tombstoneCount = ""
		resetCount = ""
		resultdata["anrCount"] = 0
		resultdata["tombstoneCount"] = 0
		resultdata["fcCount"] = 0
		resultdata["resetCount"] = 0
		isFC = False
		isTB = False
		isANR = False
		isRS = False
		stepindex = 0
		try:
			logfile = open(folder + LOG_SUFFIX, "r")
			lines = logfile.readlines()
		except IOError as e:
			lines = ""
			lines_logcat = ""
		# get case dir
		_path = folder.split(os.sep)[1:]
		resultdata["caseurl"] = os.path.join(*_path)
		# print resultdata["caseurl"]
		for line in lines:
			
			if line.find("INSTRUMENTATION_STATUS: title=") != -1:  # get case chinese name
				index = len("INSTRUMENTATION_STATUS: title=")
				casechname = line[index:].rstrip()
				resultdata["casechname"] = casechname
			elif line.find("INSTRUMENTATION_STATUS: class=") != -1:  # get case class
				index = len("INSTRUMENTATION_STATUS: class=")
				caseclass = line[index:].rstrip()
				resultdata["caseclass"] = caseclass
			elif line.find("INSTRUMENTATION_STATUS: test=") != -1:  # get case name				
				index = len("INSTRUMENTATION_STATUS: test=")
				casename = line[index:].rstrip()
				resultdata["casename"] = casename
			elif line.find("Time: ") != -1:  # record execute time
				self.summarySheet['exed'] += 1
#				self.executed += 1
				index = len("Time: ")
				exetime = line[index:].rstrip()
				resultdata["exetime"] = exetime
			elif line.find("INSTRUMENTATION_STATUS: caseStep=") != -1:  # get case step
				stepindex += 1
				line = re.sub(r'INSTRUMENTATION_STATUS: caseStep=\d?\d?\.?', str(stepindex) + '.', line, 1).rstrip()
				casestep += line + "\n"
			elif line.find("INSTRUMENTATION_STATUS: screenshot=") != -1:  # get screenshot info
				index = len("INSTRUMENTATION_STATUS: screenshot=")
				screencap = line[index:].rstrip()
				resultdata["screencap"] = screencap
			elif line.find("INSTRUMENTATION_STATUS: logstack=") != -1:  # get logstack info
				index = len("INSTRUMENTATION_STATUS: logstack=")
				logstack = line[index:].rstrip()
				resultdata["logstack"] = logstack
			elif line.find("INSTRUMENTATION_STATUS: stack=") != -1:  # record fail reason
				index = len("INSTRUMENTATION_STATUS: stack=")
				failreason = line[index:].rstrip()
				if failreason.find("ANR occurred") != -1:
					if isANR == False:
						isANR = True
						resultdata["anrCount"] += 1
						ispass = "ANR"
				elif failreason.find("FC occurred") != -1:
					if isFC == False:	
						isFC = True
						resultdata["fcCount"] += 1
						ispass = "FC"
				resultdata["failreason"] = "错误原因:\n" + failreason 
			elif line.find("INSTRUMENTATION_STATUS: TOMBSTONES=") != -1:  # get tombstone
				if isTB == False:
					isTB = True
					resultdata["tombstoneCount"] += 1
					ispass = "Tombstone"
				resultdata["failreason"] = "错误原因:\n"
			elif line.find("INSTRUMENTATION_STATUS: ANR=") != -1:  # get anr
				if isANR == False:
					isANR = True
					resultdata["anrCount"] += 1
					ispass = "ANR"
				resultdata["failreason"] = "错误原因:\n"
			elif line.find("ANR occurred") != -1:  # get anr
				if isANR == False:
					isANR = True
					resultdata["anrCount"] += 1
					ispass = "ANR"
				resultdata["failreason"] = "错误原因:\n"
			elif line.find("FC occurred") != -1:  # get fc
				if isFC == False:
					isFC = True
					resultdata["fcCount"] += 1
					ispass = "FC"
				resultdata["failreason"] = "错误原因:\n"
			elif line.find("Tombstone occurred") != -1:  # get tombstone
				if isTB == False:
					isTB = True
					resultdata["tombstoneCount"] += 1
					ispass = "Tombstone"
				resultdata["failreason"] = "错误原因:\n"
			elif line.find("Reboot occurred") != -1:  # get reboot
				if isRS == False:
					isRS = True
					resultdata["resetCount"] += 1
					ispass = "Reset"
				resultdata["failreason"] = "错误原因:\n"
			elif line.find(FLAG_PASS) != -1:  # record pass or fail
				ispass = "pass"
		resultdata["ispass"] = ispass
		resultdata["casestep"] = casestep
		if (len(exetime) == 0):
			if ispass == "fail":
				ispass = "notrun"
				resultdata["ispass"] = ispass		
		if ispass == 'pass':
			self.summarySheet['pass'] += 1
		if isFC:
			self.summarySheet['fc'] += resultdata["fcCount"]
		if isTB:
			resultdata["failreason"] += "\n Tombstone Occurred"
			self.summarySheet['tb'] += resultdata["tombstoneCount"]
		if isANR:
			resultdata["failreason"] += "\n ANR Occurred"
			self.summarySheet['anr'] += resultdata["anrCount"]
		if isRS:
			resultdata["failreason"] += "\n Reboot Occurred"
			self.summarySheet['reset'] += resultdata["resetCount"]
		if (caseclass == "" and casename == ""):
			resultdata["casename"] = folder
			resultdata["casechname"] = "case.log不存在"
		return resultdata
	
	def getResultData(self):
		return self.resultSheet
	
	def getSummaryData(self):
		self.summarySheet['exed'] = self.executed
		self.summarySheet['fail'] = self.executed - self.summarySheet['pass']
		self.summarySheet['notrun'] = int(self.summarySheet['plan']) - self.executed
		return self.summarySheet


class HtmlReport():
	def __init__(self, phoneData, dataFC, dataTB, dataANR, dataReset, totalExeTime, totalError, dataPass, dataExce, passRate, mtbfVal):
		self.phoneData = phoneData
		self.dataFC = dataFC
		self.dataTB = dataTB
		self.dataANR = dataANR
		self.dataPass = dataPass
		self.dataExce = dataExce
		self.dataReset = dataReset
		self.totalExeTime = totalExeTime
		self.totalError = totalError
		self.mtbfVal = mtbfVal
		self.passRate = passRate
		from django.conf import settings

		settings.configure(DEBUG=True, TEMPLATE_DEBUG=True,
 		    TEMPLATE_DIRS=(os.path.join(os.path.dirname(__file__), 'htmlTemplate'),))
		djangoVersion = django.get_version()[0:3]
		if djangoVersion == '1.7':
 			django.setup()
		self.t = get_template("child.html")

	def writeToFile(self, path):
		html = self.t.render(Context({"testresult":self.phoneData, "totalANR":self.dataANR, "totalTombstone":self.dataTB, "totalFC":self.dataFC, "totalReset":self.dataReset, "totalExeTime":self.totalExeTime, "totalError":self.totalError, "totalcasePass":self.dataPass, "totalcaseExce":self.dataExce, "passRate":self.passRate, "mtbfValue":self.mtbfVal}))
		now = datetime.now()
		year = now.year  
		month = now.month  
		day = now.day  
		hour = now.hour  
		minute = now.minute
		nowtime = str(year)+str(month)+str(day)+"_"+str(hour)+str(minute)  
		htmlPath = os.path.join(path,nowtime+".html")
		with open(htmlPath, 'w') as fp:
			fp.write(html)
				
def getFolderList(folder):	
		pList = []
		for f in os.listdir(folder):
			if os.path.isdir(os.path.join(folder, f)):
				pList.append(os.path.join(folder, f))
		pList.sort(key=lambda x: os.stat(x).st_ctime)
		return pList

def getLoopData(logFolder, loopC):
	caseLogList = []
	for folder in os.listdir(logFolder):
		if os.path.isdir(os.path.join(logFolder, folder)):
			caseLogList.append(os.path.join(logFolder, folder))
	caseLogList.sort(key=lambda x: os.stat(x).st_ctime)
	_p = LogParser(4, caseLogList)	
	return _p

def getBuildInfo(folder):
	try:
		phoneInfo = open(folder + "/phoneInfo.txt", "r")
		lines = phoneInfo.readlines()
	except IOError as e:
		lines = ""
	phoneVer = ""
	phoneIMEI = ""
	phoneDate = ""
	startTime = ""
	endTime = ""
	phoneExeTime = 0
	for line in lines:
		if line.find("buildVersion==") != -1:  # get build version
				index = len("buildVersion==")
				phoneVer = line[index:].rstrip()
		elif line.find("buildDate==") != -1:  # get build date
				index = len("buildDate==")
				phoneDate = line[index:].rstrip()
		elif line.find("testStartTime==") != -1:  # get start time
				index = len("testStartTime==")
				startTime = line[index:].rstrip()
		elif line.find("testEndTime==") != -1:  # get end time
				index = len("testEndTime==")
				endTime = line[index:].rstrip()
	startDateTime = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
	endDateTime = datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
	phoneExeTime = (endDateTime - startDateTime).total_seconds() / 3600
	phoneExeTime = round(phoneExeTime, 1)
	return phoneVer, phoneIMEI, phoneDate, startTime, endTime, phoneExeTime
		
			
def main(argv):
 	rootFolder = argv[1]
# 	rootFolder = "/home/lihb/MTBF_For_Phone/20141022"
	# test phone numbers
	phoneList = getFolderList(rootFolder)
# 	print phoneList
	phoneDataList = []
	phoneC = 0
	phoneFC = 0
	phoneTB = 0
	phoneReset = 0
	phoneANR = 0
	Pass = 0
	Exce = 0
	rate = 0
	casePass = 0
	caseExce = 0
	totalcasePass = 0
	totalcaseExce = 0
	totalFC = 0
	totalTB = 0
	totalANR = 0
	totalReset = 0
	totalExeTime = 0
	totalError = 0
	for phone in phoneList:
		phoneFC = 0
		phoneTB = 0
		phoneReset = 0
		phoneANR = 0
		casePass = 0
		caseExce = 0
		Pass = 0
		Exce = 0
		rate = 0
		phoneC += 1
		# phone test loops
		# cPhone = "Phone" + str(phoneC)  # current phone key
		cPhone = phone.split("/")[-1]
		loopList = getFolderList(phone)
#  		print loopList
		loopC = 0
		loopDataList = []
		for loop in loopList:
			loopC += 1
			cLoopData = getLoopData(loop, loopC)
			loopDataList.append({'loopName':"loop" + str(loopC), 'loopData':cLoopData.getResultData()})
			phoneFC += cLoopData.summarySheet['fc']
			phoneTB += cLoopData.summarySheet['tb']
			phoneANR += cLoopData.summarySheet['anr']
			phoneReset += cLoopData.summarySheet['reset']
			casePass += cLoopData.summarySheet['pass']
			caseExce += cLoopData.summarySheet['exed']
		Pass = casePass
		Exce = caseExce
		rate = '%.2f'%(casePass/caseExce*100)		
		phoneVer, phoneIMEI, phoneDate, phoneStartTime, phoneEndTime, phoneExeTime = getBuildInfo(rootFolder + "/" + cPhone)
		phoneDataList.append({'phoneName':cPhone, 'summary':{"buildDate":phoneDate, "release":phoneVer, "IMEI":phoneIMEI, "startTime":phoneStartTime, "EndTime":phoneEndTime, "exeTime":str(phoneExeTime) + "Hrs", "ANR":phoneANR, "FC":phoneFC, "Tombstone":phoneTB, "Reset":phoneReset, "Pass":Pass, "Exce":Exce, "Rate":rate}, 'phoneData':loopDataList})
		totalcasePass += casePass
		totalcaseExce += caseExce
		totalFC += phoneFC
		totalTB += phoneTB
		totalANR += phoneANR
		totalReset += phoneReset
		totalExeTime += phoneExeTime
		totalError = totalFC + totalTB + totalANR + totalReset
# 	HtmlReport(phoneDataList).writeToFile(os.path.dirname(__file__))
	if totalError > 0:
		mtbfVal = totalExeTime / totalError
	else:
		mtbfVal = totalExeTime / 1
	mtbfVal = round(mtbfVal, 1); 
	passRate = '%.2f'%(totalcasePass/totalcaseExce*100)
 	HtmlReport(phoneDataList, totalFC, totalTB, totalANR, totalReset, str(totalExeTime) + "Hrs", totalError, totalcasePass, totalcaseExce, passRate,mtbfVal).writeToFile(rootFolder)		
	
if __name__ == '__main__':
	main(sys.argv)
