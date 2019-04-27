#/usr/bin/env python
#coding: utf-8

import sys
import os
import re
import signal
import time

TIMEOUT=10 #输入10s倒计时!!! 
DEFEAULTINPUT="yes" #默认输入yes

def Usage():
	print "========================================================================"
	print "即将repo sync code, 如果要求输入的命令"+str(TIMEOUT)+"S之内没有输入,默认会自动选择"+DEFEAULTINPUT
	print "========================================================================"
	time.sleep(1)

class StdInput(object):

	def __input__(self):
		try:
			aswan=sys.stdin.readline().strip()
			return aswan
		except:
			return
	def getInput(self):
		signal.signal(signal.SIGALRM, self.__input__)
		signal.alarm(TIMEOUT)
		aswan=self.__input__()
		if aswan is None:
			return DEFEAULTINPUT
		else:
			return aswan

class GetProjectClass(object):
	Home=''
	projectList=[]
	stdinput=''

	def __init__(self):
		self.stdinput=StdInput()
		self.Home=os.path.expanduser('~')#env=os.environ['HOME'] for windows!!!
		print "Home is:"+self.Home

	def __ConstructProjectList__(self,path):
		#os.chdir(self.Home)
		Dircots=os.listdir(path)
		for direct in Dircots:
			if direct == ".repo":
				self.projectList.append(path)
				return
			elif os.path.isdir(direct):#为文件夹,继续遍历
				self.__ConstructProjectList__(path+"/"+direct)
			else:#为文件,遍历停止
				continue

	def SyncProjectList(self):
		os.chdir(self.Home)
		self.__ConstructProjectList__(self.Home)
		print "含有.repo工程的工程文件夹有以下: "
		for project in self.projectList:
			GetCode=GetCodeClass(project);
			print "工程: "+project+"  将更新"+str(TIMEOUT)+"S后默认sync"
			aswan=self.stdinput.getInput()
			if re.search("y",aswan,re.IGNORECASE):
				GetCode.Sync()
			else:
				print "放弃"+project+"工程sync"
			

class GetCodeClass(object):
    ListGitPath=[]
    ListIgnorProject=[]
    Home=""
    LocalPath=""
    syncerrorname="syncodeerror.log"
    
    def __init__(self,path):
    	self.LocalPath=path
    	self.stdinput=StdInput()

    def __doConflict__(self,proname):
    	os.chdir(self.LocalPath+"/"+proname);
    	os.system("git checkout .")
    	os.system("git clean -xdf")
    	os.system("git pull")

    def __CreateFetchingErrorProject__(self):
    	os.chdir(self.LocalPath)
    	file=open(self.syncerrorname)
    	for line in file:
    		result=re.findall(r".*error:(.*):.*",line)#注意返回的是一个list,并非字符串
    		if result:
    			self.ListGitPath.append(result[0].lstrip()); #result[0].lstrip() 为去掉字符串左边的空格

    def __conflictProject__(self,throwaway):
    	print "开始处理所有冲突的project!"
    	for projectname in self.ListGitPath:
    		if re.search("y",throwaway,re.IGNORECASE):
    			print "自动清理project: "+projectname
    		else:
    			print projectname+" 是否丢弃?留意10S后默认清理"
    			aswan=self.stdinput.getInput()
    			if re.search("y",aswan,re.IGNORECASE):
    				print "清理project: "+projectname
    			else:
    				print "忽略project: "+projectname
    				self.ListIgnorProject.append(projectname)
    				continue;
    		self.__doConflict__(projectname)
    	print "冲突解决成功!!!!!!!!!!!!!!!!!!!"
    	if len(self.ListIgnorProject):
    		print "以下project冲突被忽略:"
    		for ignorename in self.ListIgnorProject:
    			print ignorename

    def __repoSyncCode__(self):
    	os.system("repo sync 2>%s" %(self.syncerrorname))
    	self.__CreateFetchingErrorProject__()

    def __ResetconflictProject__(self):
    	if len(self.ListGitPath) == 0:
    		print "没有project有冲突,sync code 成功!!!"
    		return
    	print ".................以下project存在冲突.................."
    	for confictpath in self.ListGitPath:
    		print confictpath.lstrip()
    	print "是否全部自动全部丢弃? 留意10S后默认清理"
    	aswan=self.stdinput.getInput()
    	self.__conflictProject__(aswan)

    def Sync(self):
    	print "开始更新................"
    	os.chdir(self.LocalPath)
    	self.__repoSyncCode__()
    	self.__ResetconflictProject__()
    	if os.path.exists(self.syncerrorname):
    		os.remove(self.LocalPath+"/"+self.syncerrorname)
    	print "更新完成................"

if __name__ == '__main__':
	reload(sys);
	sys.setdefaultencoding('utf-8');
	Usage()
	Project=GetProjectClass()
	Project.SyncProjectList()