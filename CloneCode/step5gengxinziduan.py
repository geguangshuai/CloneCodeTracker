#coding=utf-8
import time
import logging
from dao import *
from ggstools import *

'''
获得片段列表 文件路径+起始行+结束行+新起始行+新结束行
'''
def getFragmentList(info):
        tmplist = info.split()
        fragmentlist = []
        for tmp in tmplist:
                fragment = tmp.split('+')
                fragmentlist.append(fragment)
        return fragmentlist

def mycmp(a, b):
        if int(a[0]) > int(b[0]):
                return 1
        else:
                return -1

'''
为了推算克隆片段的位置，获得文件变化字典
{‘filepath':[(s,e,ns,ne)]}
changelistofsamefilepath存放一个改变列表[（1354+1360+1354+1360   0），（1365+1371+1365+1371   0），（），（）]，且已经排好序了
'''
def getChangeDict(changelist):
        changedict = {}
        for change in changelist:
                filepath = changedict.get(change[0], None)
                if filepath == None:
                        move = (int(change[4]) - int(change[3])) -  (int(change[2]) - int(change[1]))
                        changedict[change[0]] = [ [int(change[1]),int(change[2]),int(change[3]),int(change[4]), move] ] #s,e,ns,ne,cl
                else:
                        move = (int(change[4]) - int(change[3])) -  (int(change[2]) - int(change[1]))
                        changedict[change[0]].append([int(change[1]),int(change[2]),int(change[3]),int(change[4]), move])
        #end for
        #对每一个文件中修改的信息，排序（按第一个字段排序即可，git diff可以保证正确性）
        #提取的是已经该序好的
#         for key in changedict.keys():
#                 changedict[key].sort(mycmp)
        return changedict


'''
判断两线段是否相交
'''
def judgeCross(a, b, c, d):
        if a > d or c > b:
                return False
        else:
                return True
        
'''
判断克隆片段是否被修改或者是否是bug
'''
def judgeCloneFragmentModifyOrBug(clonefragment, fragmentlist):
        #print '------------------------------判断是否修改了-------------------------------------'
        #print 'clonefragment info : ', clonefragment.file, clonefragment.startline, clonefragment.endline
        for fragment in fragmentlist:
                #print fragment
                if clonefragment.file == fragment[0] and judgeCross(int(clonefragment.startline), int(clonefragment.endline), int(fragment[1]), int(fragment[2])):
                        return 'yes'
        #print '----------------------------------------------------------------------------------------'
        return 'no'


'''
依据更新信息，推断克隆片段在下一版本中的位置
推算克隆片段的范围，扩大化推测，但是一定包含，后期使用位置重叠率，可以解决这个问题
changedict   {‘filepath':[(s,e,ns,ne,cl)]}
'''
def maybelocationForCloneFragment(clonefragment, changedict):
        
        changelistofsamefilepath = changedict.get(clonefragment.file, None)
              
        #如果没有修改该克隆片段所在路径，直接返回原始路径
        if changelistofsamefilepath == None:
                return clonefragment.startline + '+' + clonefragment.endline
        '''
        /src/net/sf/freecol/common/model/Unit.java+1354+1360+1354+1360   0
        /src/net/sf/freecol/common/model/Unit.java+1365+1371+1365+1371   0
        /src/net/sf/freecol/common/model/Unit.java+1421+1427+1421+1427   0
        /src/net/sf/freecol/common/model/Unit.java+1432+1438+1432+1438   0
        /src/net/sf/freecol/common/model/Unit.java+1455+1460+1455+1470   +10
        /src/net/sf/freecol/common/model/Unit.java+1465+1473+1475+1481   -2
        /src/net/sf/freecol/common/model/Unit.java+1562+1568+1570+1576   0
        /src/net/sf/freecol/common/model/Unit.java+1577+1583+1585+1591   0
        '''
        #changelistofsamefilepath存放一个改变列表[（1354+1360+1354+1360   0），（1365+1371+1365+1371   0），（），（）]，且已经排好序了
        #根据变化扩大化推算起始行
        expansionStartLine = None
        cumulativeMove = 0
        for i in range(len(changelistofsamefilepath)):
                if  int(clonefragment.startline) < int(changelistofsamefilepath[i][0]):
                        expansionStartLine =  int(clonefragment.startline) + cumulativeMove
                        break
                if int(clonefragment.startline) <= int(changelistofsamefilepath[i][1]):
                        expansionStartLine = int(changelistofsamefilepath[i][2])
                        break
                cumulativeMove = cumulativeMove + int(changelistofsamefilepath[i][4])
        #如果该克隆片段的起始行在所有修改的下面，那么expansionStartLine会等于None
        #但此时cumulativeMove已经包含了所有的累计变化
        if expansionStartLine == None:
                expansionStartLine = int(clonefragment.startline) + cumulativeMove
        #---------------------------------------------------------------------------------------------------------------------------------
        
        #根据变化扩大化推算结束行
        expansionEndLine = None
        cumulativeMove = 0
        for i in range(len(changelistofsamefilepath)):
                if  int(clonefragment.endline) < int(changelistofsamefilepath[i][0]):
                        expansionEndLine =  int(clonefragment.endline) + cumulativeMove
                        break
                if int(clonefragment.endline) <= int(changelistofsamefilepath[i][1]):
                        expansionEndLine = int(changelistofsamefilepath[i][3])
                        break
                cumulativeMove = cumulativeMove + int(changelistofsamefilepath[i][4])
        #如果该克隆片段的结束行在所有修改的下面，那么expansionEndLine会等于None
        #但此时cumulativeMove已经包含了所有的累计变化
        if expansionEndLine == None:
                expansionEndLine = int(clonefragment.endline) + cumulativeMove
        #---------------------------------------------------------------------------------------------------------------------------------

                
        return str(expansionStartLine) + '+' + str(expansionEndLine)

'''
对一个克隆片段内容token化
'''      
def makeToken(oldstr):
        symbols = ',.;:?\'"([{%^-<>!|/\\~#)]}&*=+'
        keywordDict =  {'auto' : 'A', 'struct' : 'S', 'break' : 'B', 'else' : 'E', 'switch' : 'S', 'case' : 'C', 'enum' : 'E', 'register' : 'R', 'typedef' : 'T', 'extern' : 'E', 'return' : 'R', 'union' : 'U', 'const' : 'C', 'continue' : 'C', 'for' : 'F', 'default' : 'D', 'goto' : 'G', 'sizeof' : 'S', 'volatile' : 'V', 'do' : 'D', 'while' : 'W', 'static' : 'S' }
        #第一步，对老的字符串，符号的左右加空格，形成新的字符串
        newlist = []
        for char in oldstr:
                if char in symbols:
                        newlist.append(' ' + char + ' ')
                else:
                        newlist.append(char)
        newstr = ''.join(newlist)
        #第二步，以空格分割，形成每一个单词，按规则替换
        wordlist = newstr.split()
        tokenlist = []
        strcontent = False
        for word in wordlist:
                if strcontent == True:#如果在字符串内容阶段
                        if word == '"':#如果是“，说明字符串结束了，添加S，并终止字符串阶段
                                tokenlist.append('S')
                                strcontent = False
                else:#非字符串内容阶段
                        if word == '"':
                                strcontent = True
                        else:
                                keywordvalue = keywordDict.get(word, None)
                                if keywordvalue != None:#如果是关键字（除去int、float、double等数据类型）
                                        tokenlist.append(keywordvalue)
                                        continue
                                if word[0] in '0123456789' and word[-1] in '0123456789':#如果是数字，用D替换
                                        tokenlist.append('D')
                                        continue
                                if word in symbols:#如果是符号，保留
                                        tokenlist.append(word)
                                        continue
                                tokenlist.append('V')#一般变量，用V
                        #end else 非字符串内容阶段
        #end for
        tokenstr = ''.join(tokenlist)
        return tokenstr
     
'''
统计克隆群包含的克隆片段的modify、bug个数
pcid:clonefragment
'''
def countCloneFragmentModifyAndBugOfCloneClass(cloneclass, pcid_clonefragment_dict):
        ismodify,isbug = 0,0
        pcidset = cloneclass.pcidset.split('-')
#         print cloneclass.version, cloneclass.classid
#         print pcidset
        for pcid in pcidset:
                clonefragment = pcid_clonefragment_dict[int(pcid)]
                if clonefragment.ismodify == 'yes':
                        ismodify = ismodify + 1
                if clonefragment.isbug == 'yes':
                        isbug = isbug + 1
        #克隆群至少包含两个克隆片段保证pcidset长度一定不为零
        topic = makeToken(pcid_clonefragment_dict[int(pcidset[0])].source)
        
        return_ismodify = ''
        if ismodify == 0:
                return_ismodify = 'no'
        else:
                return_ismodify = 'yes'
        
        return_isbug = ''
        if isbug == 0:
                return_isbug = 'no'
        else:
                return_isbug = 'yes'
        return topic, return_ismodify, return_isbug


'''
根据下次提交的修改信息、是否是bug修复，对当前版本的克隆片段、克隆群标注bug、修改情况
'''
def updateModifyAndBugAndMaybeLocationForVersion(versioninfo):
        changelist =  getFragmentList(versioninfo.changeinfo)
        bugfixlist = getFragmentList(versioninfo.bugfixinfo)
        changedict = getChangeDict(changelist)
        
        logging.info('update current version clonefragment : [ismodify], [isbug], [maybelocation]')
        #获得当前版本的所有克隆片段
        clonefragmentDao = CloneFragmentDao()
        clonefragmentlist = clonefragmentDao.selectAllCloneFragmentForVersion(versioninfo.version)
        #对克隆片段的ismodify、isbug、maybelocation字段更新
        for i in range(len(clonefragmentlist)):
                #判断是否修改了，依据修改代码段与该克隆片段是否有交集
                clonefragmentlist[i].ismodify = judgeCloneFragmentModifyOrBug(clonefragmentlist[i], changelist)
                #判断是否为bug，依据bugfix代码段与该克隆片段是否有交集
                clonefragmentlist[i].isbug = judgeCloneFragmentModifyOrBug(clonefragmentlist[i], bugfixlist)
                #该克隆片段到下一版本的可能位置，依据修改推移位置变化
                clonefragmentlist[i].maybelocation = maybelocationForCloneFragment(clonefragmentlist[i], changedict)
        
        #批量更新克隆片段
        clonefragmentDao.batchUpdateCloneFragment(clonefragmentlist)
        logging.info('update current version clonefragment : [ismodify], [isbug], [maybelocation]  OK')
        
        logging.info('Update some fields of the current version of clone group: [topic], [ismodify], [isbug]')
        #整理一份克隆片段字典，pcid:clonefragment
        pcid_clonefragment_dict = {}
        for i in range(len(clonefragmentlist)):
                pcid_clonefragment_dict[int(clonefragmentlist[i].pcid)] = clonefragmentlist[i]
        #获得当前版本的所有克隆群
        cloneclassDao = CloneClassDao()
        cloneclasslist = cloneclassDao.selectAllCloneClassForVersion(versioninfo.version)
        #对每个克隆群的ismodify、isbug字段更新
        for i in range(len(cloneclasslist)):
                #统计该克隆群包含的克隆片段的ismodify、isbug信息,将数量记录在克隆群的相应字段
                cloneclasslist[i].topic, cloneclasslist[i].ismodify, cloneclasslist[i].isbug = countCloneFragmentModifyAndBugOfCloneClass(cloneclasslist[i], pcid_clonefragment_dict)
#                 if cloneclasslist[i].ismodify != '0':
#                         print 'ismodify', cloneclasslist[i].version, cloneclasslist[i].classid
#                 if cloneclasslist[i].isbug != '0':
#                         print 'isbug', cloneclasslist[i].version, cloneclasslist[i].classid
        #批量更新克隆群
        cloneclassDao.batchUpdateCloneClass(cloneclasslist)
        logging.info('Update some fields of the current version of the clone group: [topic], [ismodify], [isbug] OK')
        

'''
Bug与克隆片段关联（根据下次提交修改数据，标注当前版本克隆的修改、bug信息）
'''
def updateModifyAndBugAndMaybeLocationForSoftware(software, subject,to_addr):
        #获取所有版本信息
        versioninfoDao = VersionInfoDao()
        versioninfolist = versioninfoDao.selectAllVersionInfoForSoftware(software)
        #利用修改信息标注当前版本的modify、bug、maybelocation字段(克隆片段与bug关联)
        for i in range(len(versioninfolist)):
                logging.info('Updated version of [%s] for some fields: [ismodify], [isbug], [maybelocation]' % versioninfolist[i].version)
                start = time.time()
                updateModifyAndBugAndMaybeLocationForVersion(versioninfolist[i])
                end = time.time()
                logging.info('Update field time:%s' % (end - start))
                if (i+1) % 10 == 0:
                        content = '共 %s 个版本， %s 个版本已经完成克隆字段更新' % (len(versioninfolist), str(i+1))
                        mailAlert(subject, content,to_addr)
        #end for
        return len(versioninfolist)


def main(software, ip,to_addr):
        logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                datefmt='%a, %d %b %Y %H:%M:%S',
                                filename='%s.log' % software,
                                filemode='a')
        logging.info('start update clone field')
        subject = '%s @  %s' % (software, ip)
        try:
                versionnumber = updateModifyAndBugAndMaybeLocationForSoftware(software, subject,to_addr)
                content = '所有版本字段更新完毕，共 %s 个版本' % versionnumber
                logging.info(content)
                mailAlert(subject, content,to_addr)
        except Exception, e:
                content = str(e)
                logging.info(content)
                mailAlert(subject, content,to_addr)