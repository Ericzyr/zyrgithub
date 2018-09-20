import csv
import os,sys
import time
import string
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
from django.template import Context

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
reload(sys)
sys.setdefaultencoding('utf-8')

class CsvReader():
	def __init__(self, path):
		self.csvFile = csv.DictReader(file(path, 'rb'))
		self.plist = []#cmdline names
		self.tempdict = {}
		for row in self.csvFile:
			timestamp = row['Second']
			if not self.tempdict.has_key(timestamp):
				self.tempdict[timestamp] = {}
			pname = row['cmdline']
			if not pname in self.plist:
				self.plist.append(pname)
			cpu = row['CPU%']
			self.tempdict[timestamp].update({pname:cpu})
			
	def getProcessList(self):
		if self.plist[0] != 'Second':
			self.plist.insert(0, 'Second')
		return self.plist

        def getTop5ProcessList(self,path):
		topFile = open(path+"/Pss_Cpu/name.txt","r") 
		self.toplist = []#top 5 cmdline names
		for line in topFile.readlines():
			line=line.strip('\n')
                        self.toplist.append(line)
                return self.toplist
	
	def getRowData(self):
		data = []
		for key, value in self.tempdict.items():
			value.update({'Second':key})
			data.append(value)
		data.sort(key=lambda data : int(data['Second']))
		return data			
	
class CsvWriter():
	def __init__(self, path, fieldname):
		self.writer = csv.DictWriter(file(path, 'wb'), fieldnames=fieldname,restval="0")
	
	def generateCsvFile(self, rowData):
		self.writer.writerows(rowData)
		
def main(argv):
	time1= time.time()
	if len(argv) != 4:
		print "Letv Csv format convert for chart Ver 0.1"
		print "Usage:"
		print "python cpuformatter.py <source.csv> <output.csv> <PicFolder>"
		sys.exit()
	cr = CsvReader(argv[1])
	pl = cr.getProcessList()
        tl = cr.getTop5ProcessList(argv[3])
	cw = CsvWriter(argv[3].split(os.sep)[0]+"/"+argv[2], pl)
	cw.generateCsvFile(cr.getRowData())
        tmp = get_template("htmlTemplate/topPicTemp.htm")
	rd = {'datafields':pl}        
        top = {'top5processes':tl}
        rd.update(top)
        html = tmp.render(Context(rd))
	with open(argv[3].split(os.sep)[0]+"/topPic.htm", 'w') as fp:
		fp.write(html)
	time2= time.time()
	print "convert file top.csv finished. Cost time:"+str(time2-time1)+ " sec."

if __name__ == '__main__':
	main(sys.argv)
