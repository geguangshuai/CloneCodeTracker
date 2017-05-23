#coding=utf-8
import time
import logging
from dao import *
import Levenshtein
from ggstools import *

'''
计算两个字符串的编辑距离相似度
'''
def calculateLevenshtein(s1, s2):
        fz = Levenshtein.distance(s1,s2)
        fm = len(s1)
        if len(s2) > fm:
                fm = len(s2)
        return 1.0 - 1.0*fz/fm

#目前更改为计算两个克隆片段的编辑距离
def calculateCloneClassSimilarity(b_cloneclass, c_cloneclass):
        return calculateLevenshtein(b_cloneclass.topic, c_cloneclass.topic)
        
'''
计算两个克隆片段的相似度
'''
def calculateCloneFragmentSimilarity(b_clonefragment, c_clonefragment):
#         print b_clonefragment.file, b_clonefragment.startline, b_clonefragment.endline
#         print c_clonefragment.file, c_clonefragment.startline, c_clonefragment.endline
        #文件不一致，不可能建立映射
        if b_clonefragment.file != c_clonefragment.file:
                return 0.0
        #如果两个片段大小差距大大，直接返回0
        #由于NiCad检测工具，检测出来的克隆片段具有包含关系，所以这里需要自行处理
#         sizediff = abs(len(b_clonefragment.source) - c_clonefragment.source )
#         #这里需要修改
#         if sizediff >= 20:
#                 return 0.0
        
        #b克隆片段的起始结束行使用的是推算出来的可能位置(扩大化，后期计算位置重叠率，求max、min可以缩回应该的位置)
        b_startline, b_endline = map(int, b_clonefragment.maybelocation.split('+'))
        c_startline, c_endline = map(int, (c_clonefragment.startline, c_clonefragment.endline))
        #计算位置重叠率
        overlapping = 1.0 * ( min(b_endline, c_endline) - max(b_startline, c_startline) +1) / (c_endline - c_startline+1)
        return overlapping
#         if overlapping >= 0.7:
#                 return overlapping
#         else:
#                 return calculateLevenshtein(b_clonefragment.source, c_clonefragment.source)

def sizeDiff(clonefragment1, clonefragment2):
        return Levenshtein.distance(clonefragment1.source, clonefragment2.source)
#         size1 = int(clonefragment1.endline) - int(clonefragment1.startline) + 1
#         size2 = int(clonefragment2.endline) - int(clonefragment2.startline) + 1
#         sizediff = size1 - size2
#         if sizediff < 0:
#                 sizediff = -sizediff
#         return sizediff


'''
b版本和c版本之间建立克隆映射
'''
def bVersionAndcVersionCloneMap(bversion, cversion):
        logging.info('clone class mapping')
        cloneclassDao = CloneClassDao()
        bcloneclasslist = cloneclassDao.selectAllCloneClassForVersion(bversion)
        ccloneclasslist = cloneclassDao.selectAllCloneClassForVersion(cversion)
        cloneclassmaplist = []
        #克隆群映射，根据topic字段
        for i in range(len(bcloneclasslist)):
#                 print '-'*20
#                 print 'version', bcloneclasslist[i].version
#                 print 'classid', bcloneclasslist[i].classid
                for j in range(len(ccloneclasslist)):
                        similarity = calculateCloneClassSimilarity(bcloneclasslist[i], ccloneclasslist[j])
                        if similarity >= 0.6:#改变这里是调整Token编辑距离相似度阈值，阈值已确定为0.6
                                cloneclassmap = CloneClassMap(bcloneclasslist[i].version, bcloneclasslist[i].classid, ccloneclasslist[j].version, ccloneclasslist[j].classid, str(similarity))
                                cloneclassmaplist.append(cloneclassmap)
#                                 print 'mapversion', ccloneclasslist[j].version
#                                 print 'mapclassid', ccloneclasslist[j].classid
                #end for ccloneclasslist
        #end for bcloneclasslist
        
#         #克隆群映射结果批量导入数据库
#         cloneclassmapDao =  CloneClassMapDao()
#         cloneclassmapDao.batchInsertCloneClassMap(cloneclassmaplist)
        logging.info(len(cloneclassmaplist))
        logging.info('clone class map OK')
        
        logging.info('clone fragment mapping')
        #classid : cloneclass
        b_classid_cloneclass_dict = {}
        for i in range(len(bcloneclasslist)):
                b_classid_cloneclass_dict[ int(bcloneclasslist[i].classid) ] = bcloneclasslist[i]
        c_classid_cloneclass_dict = {}
        for i in range(len(ccloneclasslist)):
                c_classid_cloneclass_dict[ int(ccloneclasslist[i].classid) ] = ccloneclasslist[i]
        #classid:[classid,classid]
        classid_mapclassidlist_dict = {}
        for i in range(len(cloneclassmaplist)):
                key = int(cloneclassmaplist[i].classid)
                value = cloneclassmaplist[i].mapclassid
                oldvalue = classid_mapclassidlist_dict.get(key, None)
                if oldvalue == None:
                        classid_mapclassidlist_dict[key] = [value]
                else:
                        classid_mapclassidlist_dict[key].append(value)

        
        #pcid:clonefragment
        clonefragmentDao = CloneFragmentDao()
        bclonefragmentlist = clonefragmentDao.selectAllCloneFragmentForVersion(bversion)
        b_pcid_clonefragment_dict = {}
        for i in range(len(bclonefragmentlist)):
                b_pcid_clonefragment_dict[int( bclonefragmentlist[i].pcid) ] = bclonefragmentlist[i]
        cclonefragmentlist = clonefragmentDao.selectAllCloneFragmentForVersion(cversion)
        c_pcid_clonefragment_dict = {}
        for i in range(len(cclonefragmentlist)):
                c_pcid_clonefragment_dict[int( cclonefragmentlist[i].pcid) ] = cclonefragmentlist[i]
        #已经准备好了
        #b_classid_cloneclass_dict（classid:cloneclass）
        #c_classid_cloneclass_dict（classid:cloneclass）
        #classid_mapclassidlist_dict（classid:[mapclassid1, mapclassid2]）
        #b_pcid_clonefragment_dict（pcid:clonefragment）
        #c_pcid_clonefragment_dict（pcid:clonefragment）
        #下面开始克隆片段映射（已建立映射的克隆群，包含的克隆片段之间做映射）
        
        clonefragmentmaplist = []
        for classid in classid_mapclassidlist_dict.keys():
#                 print 'clonefragment : classid', classid
                mapclassidlist = classid_mapclassidlist_dict[int(classid)]
                #将bversion的classid中的克隆片段，在cversion的mapclassidlist中的克隆片段中建立映射
                #bVersionAndcVersionCloneFragmentMapForCloneClass( )
                b_pcid_list = b_classid_cloneclass_dict[int(classid)].pcidset.split('-')
#                 print 'b_pcid_list', b_pcid_list
                c_pcid_list = []
                for mapclassid in mapclassidlist:
#                         if classid == 413:
#                                 print 413
#                         print '---------------------------'
#                         print mapclassid
#                         print c_classid_cloneclass_dict[int(mapclassid)].pcidset
#                         print '---------------------------'
                        c_pcid_list = c_pcid_list + c_classid_cloneclass_dict[int(mapclassid)].pcidset.split('-')
                #对b_pcid_list中的克隆片段与c_pcid_list中的克隆片段建立映射
#                 print 'b_pcid_list   ',b_pcid_list
#                 print 'c_pcid_list   ',c_pcid_list
#                 print 'c_pcid_list',c_pcid_list
                for i in range(len(b_pcid_list)):
                        #找一个最相似的
                        b_clonefragment = b_pcid_clonefragment_dict[ int(b_pcid_list[i]) ]
#                         print '给%s号克隆片段寻找映射对象' % b_pcid_list[i]
                        similarity = 0.0
                        similarity_clonefragment = None
                        sizediff = 0.0
                        for j in range(len(c_pcid_list)):
                                c_clonefragment = c_pcid_clonefragment_dict[ int(c_pcid_list[j]) ]
                                tmp_similarity = calculateCloneFragmentSimilarity(b_clonefragment, c_clonefragment)
                                tmp_sizediff = sizeDiff(b_clonefragment, c_clonefragment)
#                                 print '%s 的相似度是 %s' %  (c_clonefragment.pcid, tmp_similarity)
                                #寻找一个位置重叠率最大的，如果位置重叠了一样，那选择源码编辑距离最小的
                                if tmp_similarity > similarity or (tmp_similarity == similarity and  tmp_sizediff < sizediff):
                                        similarity = tmp_similarity
                                        similarity_clonefragment = c_clonefragment
                                        sizediff = tmp_sizediff
                        #end for 找一个最相似的
#                         if classid == 413:
#                                 print b_clonefragment.pcid, similarity_clonefragment.pcid, similarity
                        if similarity_clonefragment != None and similarity >= 1.0:#不考虑边缘扩展，位置重叠了必须为1
                                tmpcfm = CloneFragmentMap(bversion, b_clonefragment.pcid, cversion, similarity_clonefragment.pcid, str(similarity))
                                clonefragmentmaplist.append(tmpcfm)
#                                 print '最相似的是 %s  : %s' % (similarity_clonefragment.pcid, similarity)
                #end for 对b_pcid_list中的克隆片段与c_pcid_list中的克隆片段建立映射
        #end for classid_mapclassidlist_dict
        #克隆片段映射结果批量导入数据库
        clonefragmentmapDao =  CloneFragmentMapDao()
        clonefragmentmapDao.batchInsertCloneFragmentMap(clonefragmentmaplist)
        logging.info(len(clonefragmentmaplist))
        logging.info('clone fragment map OK')
        
        
        xzstart = time.time()
        #为了便于克隆群映射修正，建立字典
        #bpcid_cpcid_dict (bpcid:pcid) b版本和c版本之间所有的克隆片段映射对象
        bpcid_cpcid_dict = {}
        for clonefragmentmap in clonefragmentmaplist:
                bpcid = int(clonefragmentmap.pcid)
                cpcid = int(clonefragmentmap.mappcid)
                bpcid_cpcid_dict[bpcid] = cpcid
         
        logging.info('clone class map result fixing')
        for i in range(len(cloneclassmaplist)):
                have = False
                #判断classid与mapclassid包含的克隆片段是否具有映射关系
                classid = int(cloneclassmaplist[i].classid)
                mapclassid = int(cloneclassmaplist[i].mapclassid)
                #获取两个克隆群包含的克隆片段
                b_pcid_list = map(int, b_classid_cloneclass_dict[classid].pcidset.split('-'))
                c_pcid_list = map(int, c_classid_cloneclass_dict[mapclassid].pcidset.split('-'))
                #如果b版本的该克隆群中的有一个克隆片段的映射对象在c_pcid_list中，那么该克隆群映射正常
                for b_pcid in b_pcid_list:
                        tmp_cpcid = bpcid_cpcid_dict.get(b_pcid, None)
                        if tmp_cpcid != None and tmp_cpcid in c_pcid_list:
                                have = True
                                break
                #end for
                if have == False:
                        cloneclassmaplist[i].confirm = 'no'
        #end for
        xzend = time.time()
        logging.info('clone class map result fix cost time : %s' % str(xzend- xzstart))
        
        #克隆群映射结果批量导入数据库
        cloneclassmapDao =  CloneClassMapDao()
        for i in range(0,len(cloneclassmaplist),1000):
                if i+1000 <= len(cloneclassmaplist):
                        cloneclassmapDao.batchInsertCloneClassMap(cloneclassmaplist[i:i+1000])
                else:
                        cloneclassmapDao.batchInsertCloneClassMap(cloneclassmaplist[i:])
        
        

'''
将software软件相邻版本之间建立克隆映射
'''
def adjacentVersionCloneMapForSoftware(software, subject,to_addr):
        #获取所有版本信息
        versioninfoDao = VersionInfoDao()
        versioninfolist = versioninfoDao.selectAllVersionInfoForSoftware(software)
        #在相邻版本之间建立克隆映射
        for i in range(len(versioninfolist) - 1):
                bversion = versioninfolist[i].version
                cversion = versioninfolist[i+1].version
                logging.info('[%s] and [%s] mapping' % (bversion, cversion))
                start = time.time()
                bVersionAndcVersionCloneMap(bversion, cversion)
                end = time.time()
                logging.info('cost time : %s' % (end - start))
                
                if (i+1) % 10 == 0:
                        content = '共 %s 个版本， %s 个版本已经完成相邻版本克隆映射' % (len(versioninfolist), str(i+2))
                        mailAlert(subject, content,to_addr)
        #end for
        return len(versioninfolist)


def main(software,ip,to_addr):
        logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                datefmt='%a, %d %b %Y %H:%M:%S',
                                filename='%s.log' % software,
                                filemode='a')
        
        logging.info('start adjacent version')
        subject = '%s @  %s' % (software, ip)
        try:
                versionnumber = adjacentVersionCloneMapForSoftware(software, subject,to_addr) 
                content = '所有相邻版本之间完成克隆映射，共 %s 个版本' % versionnumber
                logging.info(content)
                mailAlert(subject, content,to_addr)
        except Exception, e:
                content = str(e)
                logging.info(content)
                mailAlert(subject, content,to_addr)