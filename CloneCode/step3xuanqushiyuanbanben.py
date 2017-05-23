#coding=utf-8
from dao import *
from ggstools import *

def makeVersionInfo(software, start, end):
        #获取所有版本提交信息
        commitDao = CommitDao()
        commitlist = commitDao.selectAllCommitForSoftware(software)
        versioninfolist = []
        #每一次提交之后，认为形成了一个新版本
        #commit : software, number, commitdate, commitid, describeinfo, changeinfo, isbugfix
        #versioninfo : software, version, commitid, cloneclassnumber, clonefragmentnumber, changeinfo, bugfixinfo
        for i in range(start-1, end):#len(commitlist)
                version = software + commitlist[i].number
                commitid = commitlist[i].commitid
                cloneclassnumber = ''
                clonefragmentnumber = ''
                changeinfo = ''
                bugfixinfo = ''
                #对于非最后一次提交的情况，将下次提交修改的信息标记在这个版本上
                if i < len(commitlist)-1:
                        changeinfo = commitlist[i+1].changeinfo
                        if commitlist[i+1].isbugfix == 'yes':
                                bugfixinfo = changeinfo
                #end if i < len(commitlist)-1 
                versioninfo = VersionInfo(software, version, commitid, cloneclassnumber, clonefragmentnumber, changeinfo, bugfixinfo)
                versioninfolist.append(versioninfo)
        #end for
        versioninfoDao = VersionInfoDao()
        versioninfoDao.batchInsertCommit(versioninfolist)
        

def main(software, start, end):
        makeVersionInfo(software,start, end)
        