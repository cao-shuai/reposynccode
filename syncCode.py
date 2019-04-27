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

class GetCodeClass(object):
    ListGitPath=[]
    ListIgnorProject=[]
    LocalPath=""
    prePath=""
    syncerrorname="syncodeerror.log"
    

    def __init__(self):
    	self.LocalPath=os.getcwd()
    	self.prePath=self.LocalPath+"/"

    def __doConflict__(self,proname):
    	os.chdir(self.LocalPath+"/"+proname);
    	os.system("git checkout .")
    	os.system("git clean -xdf")
    	os.system("git pull")

    def __input__(self):
    	try:
    		aswan=sys.stdin.readline().strip()
    		return aswan
    	except:
    		return

    def __getInput__(self):
    	signal.signal(signal.SIGALRM, self.__input__)
    	signal.alarm(TIMEOUT)
    	aswan=self.__input__()
    	if aswan is None:
    		return DEFEAULTINPUT
    	else:
    		return aswan

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
    		if re.search("yes",throwaway,re.IGNORECASE):
    			print "自动清理project: "+projectname
    		else:
    			print projectname+" 是否丢弃?留意10S后默认清理"
    			aswan=self__getInput__()
    			if re.search("yes",aswan,re.IGNORECASE):
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

    def repoSyncCode(self):
    	os.chdir(self.LocalPath)
    	os.system("repo sync 2>%s" %(self.syncerrorname))
    	self.__CreateFetchingErrorProject__()

    def ResetconflictProject(self):
    	if len(self.ListGitPath) == 0:
    		print "没有project有冲突,sync code 成功!!!"
    		return
    	print ".................以下project存在冲突.................."
    	for confictpath in self.ListGitPath:
    		print confictpath.lstrip()
    	print "是否全部自动全部丢弃? 留意10S后默认清理"
    	aswan=self.__getInput__()
    	self.__conflictProject__(aswan)

if __name__ == '__main__':
	reload(sys);
	sys.setdefaultencoding('utf-8');
	Usage()
	GetCode=GetCodeClass();
	GetCode.repoSyncCode();
	GetCode.ResetconflictProject();