#coding=utf-8
import time
import logging
from dao import *
from ggstools import *

'''
根据相邻版本克隆群映射信息，处理得到classid的字典
'''
def getCloneClassMapDict(version, mapversion):
        cloneclassmapDao = CloneClassMapDao()
        cloneclassmaplist = cloneclassmapDao.getCloneClassMapList(version, mapversion)
        bclassid_cclassidlist_dict = {} #1:[2,3]
        cclassid_bclassidlist_dict = {} #2:[1] 3:[1]
        for cloneclassmap in cloneclassmaplist:
                bclassid = int(cloneclassmap.classid)
                cclassid = int(cloneclassmap.mapclassid)
                
                oldvalue = bclassid_cclassidlist_dict.get(bclassid, None)
                if oldvalue == None:
                        bclassid_cclassidlist_dict[bclassid] = [cclassid]
                else:
                        bclassid_cclassidlist_dict[bclassid].append(cclassid)
                oldvalue = cclassid_bclassidlist_dict.get(cclassid, None)
                if oldvalue == None:
                        cclassid_bclassidlist_dict[cclassid] = [bclassid]
                else:
                        cclassid_bclassidlist_dict[cclassid].append(bclassid) 
        #end for
        return bclassid_cclassidlist_dict, cclassid_bclassidlist_dict

'''
为bclassid克隆群识别cloneclasslabel标签
'''
def getCloneClassLabel(bclassid, bclassid_cclassidlist_dict, cclassid_bclassidlist_dict):
        #如果该克隆群没有后继，为死亡模式
        successorlist = bclassid_cclassidlist_dict.get(bclassid, None)
        if successorlist == None:
                return 'death'
        
        #如果只有一个后继， 并且该后继只有一个前驱（肯定是它），为成长模式
        precursorlist = cclassid_bclassidlist_dict.get(successorlist[0])
        if len(successorlist) == 1 and len(precursorlist) == 1:
                return 'grown'
        
        #如果存在多个后继，但所有的后继都只有一个前驱（肯定是它），为分离模式
        onlyone = True
        for successor in successorlist:
                #这里可以放心的使用字典，因为一个映射，会同时在bclassid_cclassidlist_dict, cclassid_bclassidlist_dict各插入一条数据
                if len(cclassid_bclassidlist_dict[successor]) != 1:
                        onlyone = False
        if len(successorlist) >= 2 and onlyone == True:
                return 'separate'
        
        #如果只有一个后继，并且该后继有多个前驱，并且所有前驱都只有一个后继（肯定是它的后继），为合并模式
        onlyone = True
        for precursor in precursorlist:
                #这里也是放心使用的，因为这里不会是空，原因同“分离”
                if len(bclassid_cclassidlist_dict[precursor]) != 1:
                        onlyone = False
        if len(successorlist) ==  1 and len(precursorlist) >= 2 and onlyone == True:
                return 'merge'
        
        #其他情况为复杂模式
        return 'complex'

'''
获得一个版本所有克隆群的 classid：pcidlist字典
'''
def getClassidPcidSetDict(version):
        cloneclassDao = CloneClassDao()
        cloneclasslist = cloneclassDao.selectAllCloneClassForVersion(version)
        classid_pcidlist_dict = {}
        for i in range(len(cloneclasslist)):
                key = int(cloneclasslist[i].classid)
                value = map(int, cloneclasslist[i].pcidset.split('-'))
                classid_pcidlist_dict[key] = value
        return classid_pcidlist_dict

'''
获取curversion版本与nextversion版本之间的克隆片段映射
为了方便查询映射结果，做成两个字典bpcid_cpcid_dict、cpcid_bpcid_dict
'''
def getCloneFragmentMapDict(curversion, nextversion):
        clonefragmentmapDao = CloneFragmentMapDao()
        clonefragmentmaplist = clonefragmentmapDao.getCloneFragmentMapList(curversion, nextversion)
        bpcid_cpcid_dict = {} #bpcid : cpcid
        cpcid_bpcid_dict = {} #cpcid : bpcid
        #version, pcid, mapversion, mappcid, similarity
        for i in range(len(clonefragmentmaplist)):
                bpcid = int(clonefragmentmaplist[i].pcid)
                cpcid = int(clonefragmentmaplist[i].mappcid)
                bpcid_cpcid_dict[bpcid] = cpcid
                cpcid_bpcid_dict[cpcid] = bpcid
        #end for
        return bpcid_cpcid_dict, cpcid_bpcid_dict

'''
判断classid克隆群的clonefragmentlabel标签
'''
def getCloneFragmentLabel(classid, bclassid_cclassidlist_dict, bclassid_pcidlist_dict, cclassid_pcidlist_dict, bpcid_cpcid_dict, cpcid_bpcid_dict):
        #后面如果有时间可以分add、delete、keep数量分开标签(后话了)
        clonefragmentlabel = []
        #如果该克隆群中存在一个克隆片段无后继，那么为该克隆群添加delete标签
        for pcid in bclassid_pcidlist_dict[classid]:
                mappcid = bpcid_cpcid_dict.get(pcid, None)
                #如果发现一个克隆片段无后继，直接添加delete模式
                if mappcid == None:
                        clonefragmentlabel.append('delete')
                        break
        #end for
        #遍历classid映射的mapclassid，如果mapclassid克隆群中存在无前驱的克隆片段，那么为classid克隆群添加add标签
        mapclassidlist = bclassid_cclassidlist_dict.get(classid, None)
        if mapclassidlist != None:
                have = False
                for mapclassid in mapclassidlist:
                        for mappcid in cclassid_pcidlist_dict[mapclassid]:
                                pcid = cpcid_bpcid_dict.get(mappcid, None)
                                if pcid == None:
                                        clonefragmentlabel.append('add')
                                        have = True
                                        break
                        #end for mappcid
                        if have:
                                break
                #end for mapclassid
        if len(clonefragmentlabel) == 0:
                return 'keep'
        else:
                return ' '.join(clonefragmentlabel)
        
'''
判断classid克隆群的contentlabel标签
'''
def getContentLabel(bclassid, ismodify, clonefragmentlabel, bclassid_cclassidlist_dict):
        #如果没有修改，直接返回“nochange”
        if ismodify == 'no':
                return 'nochange'
        #如果该克隆群只有一个后继，并且克隆片段模式为keep或add，那么直接返回"consistent"
        successorlist = bclassid_cclassidlist_dict.get(bclassid, None)
        if successorlist != None and len(successorlist) == 1 and (clonefragmentlabel == 'keep' or clonefragmentlabel == 'add'):
                return 'consistent'
        #如果无后继，或者后继多个，或者出现了delete标签，说明“不一致变化”
        return 'inconsistent'
                

'''
借助于curversion与nextversion相邻版本的克隆映射，在curversion版本的所有克隆群上添加短期演化模式标签
'''
def addShortEvolvePatternForCurVersion(curversion, nextversion):
        #获得当前版本的所有克隆群
        cloneclassDao = CloneClassDao()
        curversioncloneclasslist = cloneclassDao.selectAllCloneClassForVersion(curversion)
        
        #为了快速识别cloneclasslabel，建立映射classid-mapclassidlist字典，减少数据库交互时间消耗
        #bclassid_cclassidlist_dict    bclassid:[cclassid1, cclassid2]  b表示当前版本
        #cclassid_bclassidlist_dict    cclassid:[bclassid1, bclassid2]  c表示后期版本
        bclassid_cclassidlist_dict, cclassid_bclassidlist_dict = getCloneClassMapDict(curversion, nextversion)
        
        #为了方便识别clonefragmentlabel，建立classid-pcidlist的映射字典、bpcid-cpcid、cpcid-bpcid的映射字典
        #bclassid_pcidlist_dict bclassid:[pcid1,pcid2]
        #cclassid_pcidlist_dict cclassid:[pcid1,pcid2]
        #bpcid_cpcid_dict   bpcid : cpcid
        #cpcid_bpcid_dict   cpcid : bpcid
        bclassid_pcidlist_dict = getClassidPcidSetDict(curversion)
        cclassid_pcidlist_dict = getClassidPcidSetDict(nextversion)
        bpcid_cpcid_dict, cpcid_bpcid_dict = getCloneFragmentMapDict(curversion, nextversion)
        cloneclassshortevolvepatternlist = []
        #为当前版本的每个克隆群添加短期演化模式标签
        #version, classid, cloneclasslabel, clonefragmentlabel, ismodify, isbug, clonegenealogyid
        for i in range(len(curversioncloneclasslist)):
                cloneclasslabel = getCloneClassLabel(int(curversioncloneclasslist[i].classid), bclassid_cclassidlist_dict, cclassid_bclassidlist_dict)
                clonefragmentlabel = getCloneFragmentLabel(int(curversioncloneclasslist[i].classid), bclassid_cclassidlist_dict, bclassid_pcidlist_dict, cclassid_pcidlist_dict, bpcid_cpcid_dict, cpcid_bpcid_dict)
                contentlabel = getContentLabel(int(curversioncloneclasslist[i].classid), curversioncloneclasslist[i].ismodify, clonefragmentlabel, bclassid_cclassidlist_dict)
                cloneclassshortevolvepattern = CloneClassShortEvolvePattern(curversion, curversioncloneclasslist[i].classid, cloneclasslabel, clonefragmentlabel, contentlabel, curversioncloneclasslist[i].ismodify, curversioncloneclasslist[i].isbug)
                
                cloneclassshortevolvepatternlist.append(cloneclassshortevolvepattern)
        #end for
        #批量导入克隆群短期演化模式（加了标签的克隆群）
        cloneclassshortevolvepatternDao = CloneClassShortEvolvePatternDao()
        cloneclassshortevolvepatternDao.batchInsertCloneClassShortEvolvePattern(cloneclassshortevolvepatternlist)
        
        
'''
为软件的最后一个版本的克隆群添加“pending”标签,CloneClassShortEvolvePattern
'''
def addShortEvolvePatternForLastVersion(lastversion):
        cloneclassDao = CloneClassDao()
        lastversioncloneclasslist = cloneclassDao.selectAllCloneClassForVersion(lastversion)
        cloneclassshortevolvepatternlist = []
        cloneclasslabel = 'pending'
        clonefragmentlabel = 'pending'
        contentlabel = 'pending'
        for i in range(len(lastversioncloneclasslist)):
                cloneclassshortevolvepattern = CloneClassShortEvolvePattern(lastversion, lastversioncloneclasslist[i].classid, cloneclasslabel, clonefragmentlabel, contentlabel, lastversioncloneclasslist[i].ismodify, lastversioncloneclasslist[i].isbug)
                cloneclassshortevolvepatternlist.append(cloneclassshortevolvepattern)
        #end for
        #批量导入克隆群短期演化模式（加了标签的克隆群）
        cloneclassshortevolvepatternDao = CloneClassShortEvolvePatternDao()
        cloneclassshortevolvepatternDao.batchInsertCloneClassShortEvolvePattern(cloneclassshortevolvepatternlist)  


'''
为整个软件的所有克隆群添加短期演化模式标签
'''
def addShortEvolvePatternForSoftware(software, subject,to_addr):
        #获取所有版本信息
        versioninfoDao = VersionInfoDao()
        versioninfolist = versioninfoDao.selectAllVersionInfoForSoftware(software)
        #每一次提交就形成一个新版本，根据当前版本与后期版本相邻映射识别短期演化模式，并标注在前期版本上
        for i in range(len(versioninfolist)-1):
                curversion = versioninfolist[i].version
                nextversion = versioninfolist[i+1].version
                logging.info('add short evolve pattern for [%s], use [%s] and [%s] map result' % (curversion, curversion, nextversion))
                start = time.time()
                addShortEvolvePatternForCurVersion(curversion, nextversion)
                end = time.time()
                logging.info('cost time : %s' % (end-start))
                
                if (i+1) % 10 == 0:
                        content = '共 %s 个版本， 根据相邻版本克隆映射，%s 个版本已经完成短期演化模式添加' % (len(versioninfolist), str(i+1))
                        mailAlert(subject, content,to_addr)
                        
        #end for
        #最后一个版本的克隆群全部添加死亡模式或者待定模式
        curversion = versioninfolist[-1].version
        logging.info('add short evolve pattern for last version [%s]'  % curversion)
        start = time.time()
        #单独处理最后一个版本的情况，克隆群、克隆片段都添加待定模式
        addShortEvolvePatternForLastVersion(curversion)
        end = time.time()
        logging.info('cost time : %s' % (end-start))
        
        content = '共 %s 个版本， 最后一个版本默认添加 [等待] 短期演化模式' % len(versioninfolist)
        mailAlert(subject, content,to_addr)
        
        return len(versioninfolist)
        
def main(software, ip,to_addr):
        logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                datefmt='%a, %d %b %Y %H:%M:%S',
                                filename='%s.log' % software,
                                filemode='a')
        logging.info('Add short evolution model')
        subject = '%s @  %s' % (software, ip)
        try:
                versionnumber = addShortEvolvePatternForSoftware(software, subject,to_addr)
                content = '根据相邻版本克隆映射，短期演化模式已全部添加在前期版本克隆群上，共 %s 个版本' % versionnumber
                logging.info(content)
                mailAlert(subject, content,to_addr)
        except Exception, e:
                content = str(e)
                logging.info(content)
                mailAlert(subject, content,to_addr)