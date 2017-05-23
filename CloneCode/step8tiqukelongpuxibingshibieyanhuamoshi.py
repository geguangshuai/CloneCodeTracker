#coding=utf-8
import time
import Queue
import logging
from dao import *
from bean import *
from ggstools import *

'''
获得与某个克隆群有关联的克隆群列表
'''
def getConnectedCloneClassShortEvolvePatternList(cloneclassshortevolvepattern):
        cloneclassshortevolvepatternlist = []
        cloneclassmapDao = CloneClassMapDao()
        cloneclassshortevolvepatternDao = CloneClassShortEvolvePatternDao()
    
        #获取所有后继克隆群
        successorlist = cloneclassmapDao.getSuccessorListUsePrecursor(cloneclassshortevolvepattern.version, cloneclassshortevolvepattern.classid)
        for successor in successorlist:
                tmpccsep = cloneclassshortevolvepatternDao.getCloneClassShortEvolvePattern(successor[0], successor[1])
#                 if tmpccsep == None:
#                         print 'successorlist', successor[0], successor[1]
                cloneclassshortevolvepatternlist.append(tmpccsep)
    
        #获取所有前驱克隆群
        precursorlist = cloneclassmapDao.getPrecursorListUseSuccessor(cloneclassshortevolvepattern.version, cloneclassshortevolvepattern.classid)
        for precursor in precursorlist:
                tmpccsep = cloneclassshortevolvepatternDao.getCloneClassShortEvolvePattern(precursor[0], precursor[1])
#                 if tmpccsep == None:
#                         print 'precursorlist ', precursor[0], precursor[1]
                cloneclassshortevolvepatternlist.append(tmpccsep)
        
        return cloneclassshortevolvepatternlist

'''
统计一个连通子图中各顶点度的总和
'''
def countTotalDegreeOfCloneGenealogy(clonegenealogy):
        cloneclassmapDao = CloneClassMapDao()
        cloneclassshortevolvepatternDao = CloneClassShortEvolvePatternDao()
        cloneclassshortevolvepatternlist = cloneclassshortevolvepatternDao.getAllCloneClassShortEvolvePatternForCloneGenealogyId(clonegenealogy.clonegenealogyid)
        totaldegree = 0
        for ccsep in  cloneclassshortevolvepatternlist:
                degree = cloneclassmapDao.getDegreeOfCloneClass(ccsep.version, ccsep.classid)
                totaldegree = totaldegree + int(degree)
        return totaldegree

'''
识别某个克隆谱系的长期演化模式
如果包含复杂，直接判定为混合   mixture
如果只有成长、死亡，判定为常规 general
如果只有成长、死亡、分离，判定为独立 independent 
如果只有成长、死亡、合并，判定为合并 merge
如果同时包含分离和合并，需要识别是否有环，
        有环为复合 reconsolidation
        无环为自由 freedom
deathnumbe='0', grownnumber='0', separatenumbe='0', mergenumbe='0', complexnumber='0'
'''
def identifyLongEvolvePatternForOneCloneGenealogy(clonegenealogy):
        if int(clonegenealogy.complexnumber) > 0:
                longevolvepattern = 'mixture'
                return longevolvepattern
        if int(clonegenealogy.separatenumber) == 0 and int(clonegenealogy.mergenumber) == 0 and int(clonegenealogy.complexnumber) == 0:
                longevolvepattern = 'general'
                return longevolvepattern
        if int(clonegenealogy.separatenumber) > 0 and int(clonegenealogy.mergenumber) == 0 and int(clonegenealogy.complexnumber) == 0:
                longevolvepattern = 'independent'
                return longevolvepattern
        if int(clonegenealogy.mergenumber) > 0 and int(clonegenealogy.separatenumber) == 0 and int(clonegenealogy.complexnumber) == 0:
                longevolvepattern = 'merge'
                return longevolvepattern
        if int(clonegenealogy.separatenumber) > 0 and int(clonegenealogy.mergenumber) > 0 and int(clonegenealogy.complexnumber) == 0:
                #如果包含分离、合并，不包含复杂，那么可能为自由或者复合，要根据是否存在环判断
                #判断是否包含环，使用点的数量与边的数量的关系即可，如果点的数量比边的数量大一那么为一棵树无环，如果边的数量大于等于点的数量则为有环
                totaldegree = countTotalDegreeOfCloneGenealogy(clonegenealogy)
                edgenumber = totaldegree/2
                vertexnumber = int(clonegenealogy.grownnumber) + int(clonegenealogy.deathnumber) + int(clonegenealogy.separatenumber) + int(clonegenealogy.mergenumber) + int(clonegenealogy.complexnumber)
        if edgenumber >= vertexnumber:
                longevolvepattern = 'reconsolidation'
        else:
                longevolvepattern = 'freedom'
        return longevolvepattern

'''
从一个引子出发，提取整个克隆谱系
（标记该点所在的连通子图的所有点）
'''
def useBFSextractOneCloneGenealogy(software, clonegenealogyid, cloneclassshortevolvepattern):
        cloneclassshortevolvepatternDao = CloneClassShortEvolvePatternDao()
        #创建一个克隆谱系，里面包含的克隆群数量为零
        clonegenealogy = CloneGenealogy(software, clonegenealogyid)
#         updatecloneclassshortevolvepatternlist = []
        q = Queue.Queue()
        #更新clonegenealogyid属性， 并加入更新的行列
        cloneclassshortevolvepattern.clonegenealogyid = clonegenealogyid
        cloneclassshortevolvepatternDao.updateOneCloneClassShortEvolvePattern(cloneclassshortevolvepattern)
#         updatecloneclassshortevolvepatternlist.append(cloneclassshortevolvepattern)
        #加入克隆谱系
        clonegenealogy.addOneCloneClassShortEvolvePattern(cloneclassshortevolvepattern)
        #加入队列
        q.put(cloneclassshortevolvepattern)
    
        while q.empty() == False:
                front = q.get()
                #获得与front连通的克隆群短期演化模式列表
#                 s2 = time.time()
                cloneclassshortevolvepatternlist = getConnectedCloneClassShortEvolvePatternList(front)
#                 e2 = time.time()
#                 print u'获取和队头关联的点，花费时间 ： %s' % (e2 - s2)
                for i in  range(len(cloneclassshortevolvepatternlist)):
                        #在所有与之关联的克隆群(克隆群短期演化模式)中，如果某个克隆群没被标注，就加入队列
                        if cloneclassshortevolvepatternlist[i].clonegenealogyid == '':
                                #更新clonegenealogyid属性， 并加入更新的行列
                                cloneclassshortevolvepatternlist[i].clonegenealogyid = clonegenealogyid
                                cloneclassshortevolvepatternDao.updateOneCloneClassShortEvolvePattern(cloneclassshortevolvepatternlist[i])
#                                 updatecloneclassshortevolvepatternlist.append(cloneclassshortevolvepatternlist[i])
                                #加入克隆谱系
                                clonegenealogy.addOneCloneClassShortEvolvePattern(cloneclassshortevolvepatternlist[i])
                                #加入队列
                                q.put(cloneclassshortevolvepatternlist[i])
                #end for
        #end while
#         #数据库更新cloneclassshortevolvepattern表
#         cloneclassshortevolvepatternDao = CloneClassShortEvolvePatternDao()
#         cloneclassshortevolvepatternDao.batchUpdateCloneClassShortEvolvePattern(updatecloneclassshortevolvepatternlist)
        #根据包含的克隆群标签种类数量识别长期演化模式
        longevolvepattern = identifyLongEvolvePatternForOneCloneGenealogy(clonegenealogy)
#         print longevolvepattern
        clonegenealogy.longevolvepattern = longevolvepattern
        #数据库插入一条clonegenealogy
        clonegenealogyDao = CloneGenealogyDao()
        clonegenealogyDao.insertOneCloneGenealogy(clonegenealogy)
        
             
             
'''
对于某个软件，在多版本中提取所有克隆谱系
（在非连通图中提取所有的连通子图并编号）
'''
def extractAllCloneGenealogyForSoftware(software, subject, to_addr):
        #获取所有版本
        versioninfoDao = VersionInfoDao()
        versioninfolist = versioninfoDao.selectAllVersionInfoForSoftware(software)

        cloneclassshortevolvepatternDao = CloneClassShortEvolvePatternDao()
        clonegenealogyid = 0
        #从前期版本开始，寻找克隆谱系的引子
        for i in range(len(versioninfolist)):
                version = versioninfolist[i].version
                #从当前版本中搜寻一个为标记的克隆群，作为新克隆谱系的引子
                cloneclassshortevolvepattern = cloneclassshortevolvepatternDao.getOneNewCloneClassShortEvolvePattern(version, '')
                while cloneclassshortevolvepattern != None :
                        #找到了一个引子
                        clonegenealogyid = clonegenealogyid + 1
                        #接下来使用BFS在整个图中，将与之关联的点全部标记
                        useBFSextractOneCloneGenealogy(software, str(clonegenealogyid), cloneclassshortevolvepattern)
                        #在该版本中集训寻找新引子
                        cloneclassshortevolvepattern = cloneclassshortevolvepatternDao.getOneNewCloneClassShortEvolvePattern(version, '')
                        
                        if clonegenealogyid % 10 == 0:
                                content = '已经提取了 %s 个克隆谱系' % clonegenealogyid
                                mailAlert(subject, content, to_addr)
                                logging.info(content)
                                
                #end while
                #此版本没有了，就在下一版本继续寻找
                
#                 if (i+1) % 1 == 0:
#                         content = '%s version,%s version  has been searched' % (len(versioninfolist), str(i+1))
#                         mailAlert(subject, content, to_addr)
#                         logging.info(content)
                        
        #end for
        logging.info('Clone clonegenealogy completed')
        return len(versioninfolist), clonegenealogyid


def main(software, ip, to_addr):
        logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                datefmt='%a, %d %b %Y %H:%M:%S',
                                filename='%s.log' % software,
                                filemode='a')

        logging.info('Start extraction clonegenealogy')
        subject = '%s @  %s' % (software, ip)
        try:
                versionnumber, clonegenealogynumber = extractAllCloneGenealogyForSoftware(software, subject, to_addr)
                content = '在 %s 个版本演化过程中，共包含 %s 个克隆谱系' % (versionnumber, clonegenealogynumber)
                logging.info(content)
                mailAlert(subject, content, to_addr)
        except Exception, e:
                content = str(e)
                logging.info(content)
                mailAlert(subject, content, to_addr)