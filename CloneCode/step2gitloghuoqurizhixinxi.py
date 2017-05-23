#coding=utf-8
import os
import re
import time
import shutil
import os.path
from bean import *
from dao import *
from ggstools import *

'''
@@ -89,7 +89,7 @@ 开头的行
返回(开始行，结束行， 新开始行， 新结束行)
'''
def reMatchChangeLine(string):
        start, end, newstart, newend = '0', '0','0', '0'
        
        #标准的格式@@ -1,6 +1,7 @@
        pattern1 = r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@.*'
        matchObj1 = re.match(pattern1, string)
        if matchObj1 != None:
                a, b, c, d = map(int, matchObj1.groups())
                start, end, newstart, newend = str(a), str(a+b-1), str(c), str(c+d-1)
                return start, end, newstart, newend
        
        #前端一行的格式@@ -1 +1,7 @@
        pattern2 = r'@@ -(\d+) \+(\d+),(\d+) @@.*'
        matchObj2 = re.match(pattern2, string)
        if matchObj2 != None:
                a, c, d = map(int, matchObj2.groups())
                start, end, newstart, newend = str(a), str(a), str(c), str(c+d-1)
                return start, end, newstart, newend
        
        #后端一行的格式@@ -1,6 +1 @@
        pattern3 = r'@@ -(\d+),(\d+) \+(\d+) @@.*'
        matchObj3 = re.match(pattern3, string)
        if matchObj3 != None:
                a, b, c = map(int, matchObj3.groups())
                start, end, newstart, newend = str(a), str(a+b-1), str(c), str(c)
                return start, end, newstart, newend
        
        #前后端都一行的格式@@ -1,6 +1 @@
        pattern4 = r'@@ -(\d+) \+(\d+) @@.*'
        matchObj4 = re.match(pattern4, string)
        if matchObj4 != None:
                a, c= map(int, matchObj4.groups())
                start, end, newstart, newend = str(a), str(a), str(c), str(c)
                return start, end, newstart, newend
        
        return start, end, newstart, newend
        
'''
diff --git a/java/org/apache/jasper/JspCompilationContext.java b/java/org/apache/jasper/JspCompilationContext.java
index 01473b0..672e376 100644
--- a/java/org/apache/jasper/JspCompilationContext.java
+++ b/java/org/apache/jasper/JspCompilationContext.java
@@ -89,7 +89,7 @@ public class JspCompilationContext {
返回一个列表 [文件路径+开始行+结束行+新开始行+新结束行]
'''
def dealWithOneCommitDetail(commitLogPath):
        fr = open(commitLogPath,'r')
        lines = fr.readlines()
        fr.close()
        changeList = []
        filePath = None
        for line in lines:
                line = line.strip()
                if line.startswith('diff --git'):
                        filePath = line.split()[2] #a/java/org/apache/jasper/JspCompilationContext.java
                        continue
                if filePath != None:
                        if line.startswith('@@ '):#以@@开头的行会包含修改信息
                                start, end, newstart, newend = reMatchChangeLine(line)
                                if start == '0': #对于新增的文件
                                        end = '0'
                                if newstart == '0':#对于删除的文件
                                        newend = '0'
                                oneChange = filePath[1:] + '+' + start + '+' + end + '+' + newstart + '+' + newend
                                changeList.append(oneChange)
                        #end if line.startswith('@@ ')
        #end for line in lines 
        return changeList

'''
获取修改信息
'''
def getChangeInfo(masterpath, commitid, tmppath):
        tmpsavedirpath = os.path.join(tmppath, 'gitshow')
        if not os.path.exists(tmpsavedirpath):
                os.mkdir(tmpsavedirpath)
        tmpsavelogpath = os.path.join(tmpsavedirpath, commitid)
        if os.path.exists(tmpsavelogpath):
                os.remove(tmpsavelogpath)
                
        os.chdir(masterpath)
        git_show_cmd = 'git show %s > %s' % (commitid, tmpsavelogpath)
        result = os.system(git_show_cmd)
        if result == 0:
                #print 'git show success'
                pass
        else:
                print 'git show fail'
                print git_show_cmd
        
        #处理修改记录，获取changelist
        #文件路径+开始行+结束行+新开始行+新结束行
        changeList = dealWithOneCommitDetail(tmpsavelogpath)
        os.remove(tmpsavelogpath)
        return ' '.join(changeList)

'''
检查提交描述是否包含bug信息
'''
def checkDescribe(describeString):
        if 'issue' in describeString:
                return 'yes'
        if 'Issue' in describeString:
                return 'yes'
        if 'fixes' in describeString:
                return 'yes'
        if 'Fixes' in describeString:
                return 'yes'
        if 'fix' in describeString:
                return 'yes'
        if 'Fix' in describeString:
                return 'yes'
        if 'bug' in describeString:
                return 'yes'
        if 'Bug' in describeString:
                return 'yes'
        if 'https://bz.apache.org/bugzilla/show_bug.cgi?id=' in describeString:
                return 'yes'
        if 'http://issues.apache.org/bugzilla/show_bug.cgi?id=' in describeString:
                return 'yes'
        if 'Bugzilla' in describeString:
                return 'yes'
        if re.match(r'.*(bug *\d+)\D+.*', describeString) != None:
                return 'yes'
        return 'no'

'''
使用git log提取提交日志信息
'''
def extractCommitList(software, gitcodepath, tmppath):
        #获取commit log信息放在commit.list中
        if not os.path.isdir(tmppath):
                os.mkdir(tmppath)
        commitloglistpath = os.path.join(tmppath, 'commitlog.list')
        #进入git主目录，执行git log命令
        masterpath = os.path.join(gitcodepath, software)
        os.chdir(masterpath)
        git_log_cmd = 'git log --reverse --pretty=format:"commitdate:%%ci%%ncommitid:%%H%%ndescribeinfo:%%s%%n" >  %s'  %  commitloglistpath
        result  = os.system(git_log_cmd)
        if result == 0:
                pass
        else:
                return False, 0
        #commitlog.list生成CommitList
        fr = open(commitloglistpath,'r')
        lines = fr.readlines()
        fr.close()
        
        commitlist = []
        number = 0
        
        for i in range(0, len(lines), 4):
                number = number + 1
                commitdate = lines[i].strip()[len('commitdate:'):]
                commitid = lines[i+1].strip()[len('commitid:'):]
                describeinfo = lines[i+2].strip()[len('describeinfo:'):]
                changeinfo = getChangeInfo(masterpath, commitid, tmppath)

                isbugfix = checkDescribe(describeinfo)
                commitlist.append(Commit(software, str(number), commitdate, commitid, describeinfo, changeinfo, isbugfix))
                #每500个导入一次
                if number % 500 == 0:
                        commitDao = CommitDao()
                        commitDao.batchInsertCommit(commitlist)
                        commitlist = []
                        print number
        #end for
        if len(commitlist) > 0:
                commitDao = CommitDao()
                commitDao.batchInsertCommit(commitlist)
                
        #返回总提交次数
        return True, str(len(lines)/4)
        

def main(software, workhome):
        gitcodedirpath = os.path.join(workhome, 'gitcode')
        tmppath = os.path.join(workhome, 'tmp')
        return extractCommitList(software, gitcodedirpath, tmppath)