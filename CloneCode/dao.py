#coding=utf-8
import time
import DBmanager
from bean import *

class CommitDao(object):
        '''
        可以考虑创建Dao的时候，传入cursor，
        '''
        def __init__(self):
                pass
        '''
        批量插入提交数据
        '''
        def batchInsertCommit(self, commitlist):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_insert = 'insert into commit(software, number, commitdate, commitid, describeinfo, changeinfo, isbugfix) values(%s, %s, %s, %s, %s, %s, %s)'
                sql_list = []
                for commit in commitlist:
                        sql_list.append( (commit.software, commit.number, commit.commitdate, commit.commitid, commit.describeinfo, commit.changeinfo, commit.isbugfix))
                try:
                        cursor.executemany(sql_insert, sql_list)
                        conn.commit()
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close() 
        
        '''
        根据software、number、commitid获取一个commmit对象
        '''
        def selectCommit(self, software, number, commitid):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_select = 'select software, number, commitdate, commitid, describeinfo, changeinfo, isbugfix from commit where software=%s and number=%s and commitid=%s'
                sql_tuple = (software, number, commitid)
                try:
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchone()
                        if result != None:
                                return Commit(result[0], result[1], result[2], result[3], result[4], result[5], result[6])
                        else:
                                return None
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close()
                        
        '''
        获取某software的所有提交
        '''
        def selectAllCommitForSoftware(self, software):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_select = 'select software, number, commitdate, commitid, describeinfo, changeinfo, isbugfix from commit where software=%s'
                sql_tuple = (software,)
                try:
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchall()
                        commitlist = []
                        for one in result:
                                commitlist.append(Commit(one[0], one[1], one[2], one[3], one[4], one[5], one[6]))
                        return commitlist
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close()


class VersionInfoDao(object):
        def __init__(self):
                pass
        '''
        插入一个版本信息对象
        '''
        def insertOneVersionInfo(self, versioninfo):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_insert = 'insert into versioninfo(software, version, commitid, cloneclassnumber, clonefragmentnumber, changeinfo, bugfixinfo) values(%s, %s, %s, %s, %s, %s, %s)'
                sql_tuple = (versioninfo.software, versioninfo.version, versioninfo.commitid, versioninfo.cloneclassnumber, versioninfo.clonefragmentnumber, versioninfo.changeinfo, versioninfo.bugfixinfo)
                try:
                        cursor.execute(sql_insert, sql_tuple)
                        conn.commit()
                        #print '插入成功！！！'
                except Exception as e:
                        conn.rollback()
                        print e
                        #print '插入失败！！！'
                finally:
                        cursor.close()
                        conn.close()
        
        '''
        批量插入版本信息
        '''
        def batchInsertCommit(self, versioninfolist):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_insert = 'insert into versioninfo(software, version, commitid, cloneclassnumber, clonefragmentnumber, changeinfo, bugfixinfo) values(%s, %s, %s, %s, %s, %s, %s)'
                sql_list = []
                for versioninfo in versioninfolist:
                        sql_list.append( (versioninfo.software, versioninfo.version, versioninfo.commitid, versioninfo.cloneclassnumber, versioninfo.clonefragmentnumber, versioninfo.changeinfo, versioninfo.bugfixinfo))
                try:
                        cursor.executemany(sql_insert, sql_list)
                        conn.commit()
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close() 
        
        '''
        获取某software的所有版本
        '''
        def selectAllVersionInfoForSoftware(self, software):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_select = 'select software, version, commitid, cloneclassnumber, clonefragmentnumber, changeinfo, bugfixinfo from versioninfo where software=%s'
                sql_tuple = (software,)
                try:
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchall()
                        versioninfolist = []
                        for one in result:
                                versioninfolist.append(VersionInfo(one[0], one[1], one[2], one[3], one[4], one[5], one[6]))
                        return versioninfolist
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close()
        
        '''
        批量更新版本的克隆群及克隆片段数量
        '''
        def batchUpdateNumberForSoftware(self, versioninfolist):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_insert = 'update versioninfo set cloneclassnumber=%s, clonefragmentnumber=%s where software=%s and version=%s'
                sql_list = []
                for versioninfo in versioninfolist:
                        sql_list.append( (versioninfo.cloneclassnumber, versioninfo.clonefragmentnumber, versioninfo.software, versioninfo.version))
                try:
                        cursor.executemany(sql_insert, sql_list)
                        conn.commit()
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close() 
                        
        '''
        更新一个版本的克隆群及克隆片段数量
        '''
        def updateNumberForVersion(self, versioninfo):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_insert = 'update versioninfo set cloneclassnumber=%s, clonefragmentnumber=%s where version=%s'
                sql_list =  (versioninfo.cloneclassnumber, versioninfo.clonefragmentnumber, versioninfo.version)
                try:
                        cursor.execute(sql_insert, sql_list)
                        conn.commit()
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close()
                           

class CloneFragmentDao(object):
        def __init__(self):
                pass
        '''
        批量插入克隆片段数据
        '''
        def batchInsertCloneFragment(self, clonefragmentlist):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_insert = 'insert into clonefragment(version, pcid, file, startline, endline, source, ismodify, isbug, maybelocation) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                sql_list = []
                for clonefragment in clonefragmentlist:
                        sql_list.append( (clonefragment.version, clonefragment.pcid, clonefragment.file, clonefragment.startline, clonefragment.endline, clonefragment.source, clonefragment.ismodify, clonefragment.isbug, clonefragment.maybelocation))
                try:
                        cursor.executemany(sql_insert, sql_list)
                        conn.commit()
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close() 
        
        '''
        根据version获取所有的克隆片段
        '''
        def selectAllCloneFragmentForVersion(self, version):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_select = 'select version, pcid, file, startline, endline, source, ismodify, isbug, maybelocation from clonefragment where version=%s'
                sql_tuple = (version,)
                try:
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchall()
                        clonefragmentlist = []
                        for one in result:
                                clonefragmentlist.append(CloneFragment(one[0], one[1], one[2], one[3], one[4], one[5], one[6], one[7], one[8]))
                        return clonefragmentlist
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close()
         
        '''
        批量更新克隆片段数据
        '''
        def batchUpdateCloneFragment(self, clonefragmentlist):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_insert = 'update clonefragment set ismodify=%s, isbug=%s, maybelocation=%s where version=%s and pcid=%s'
                sql_list = []
                for clonefragment in clonefragmentlist:
                        sql_list.append( (clonefragment.ismodify, clonefragment.isbug, clonefragment.maybelocation, clonefragment.version, clonefragment.pcid))
                try:
                        cursor.executemany(sql_insert, sql_list)
                        conn.commit()
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close() 
        
        def getSource(self, version, pcid):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_select = 'select source from clonefragment where version=%s and pcid=%s'
                sql_tuple = (version,pcid)
                try:
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchone()
                        if result == None:
                                return None
                        return result[0]
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close()
                        
class CloneClassDao(object):
        def __init__(self):
                pass
        '''
        批量插入克隆群数据
        '''
        def batchInsertCloneClass(self, cloneclasslist):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_insert = 'insert into cloneclass(version, classid, nclones, nlines, similarity, pcidset, topic, ismodify, isbug) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                sql_list = []
                for cloneclass in cloneclasslist:
                        sql_list.append( (cloneclass.version, cloneclass.classid, cloneclass.nclones, cloneclass.nlines, cloneclass.similarity, cloneclass.pcidset, cloneclass.topic, cloneclass.ismodify, cloneclass.isbug))
                try:
                        cursor.executemany(sql_insert, sql_list)
                        conn.commit()
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close() 
        
        '''
        批量更新克隆群数据
        '''
        def batchUpdateCloneClass(self, cloneclasslist):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_insert = 'update cloneclass set topic=%s, ismodify=%s, isbug=%s where version=%s and classid=%s'
                sql_list = []
                for cloneclass in cloneclasslist:
                        sql_list.append( (cloneclass.topic, cloneclass.ismodify, cloneclass.isbug, cloneclass.version, cloneclass.classid))
                try:
                        cursor.executemany(sql_insert, sql_list)
                        conn.commit()
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close() 
                        
                        
        '''
        根据version获取所有的克隆群
        '''
        def selectAllCloneClassForVersion(self, version):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_select = 'select version, classid, nclones, nlines, similarity, pcidset, topic, ismodify, isbug from cloneclass where version=%s'
                sql_tuple = (version,)
                try:
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchall()
                        cloneclasslist = []
                        for one in result:
                                cloneclasslist.append(CloneClass(one[0], one[1], one[2], one[3], one[4], one[5], one[6], one[7], one[8]))
                        return cloneclasslist
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close()
        
        '''
        根据version、classid获取克隆群
        '''
        def selectCloneClassForVersionAndClassid(self, version,classid):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_select = 'select version, classid, nclones, nlines, similarity, pcidset, topic, ismodify, isbug from cloneclass where version=%s and classid=%s'
                sql_tuple = (version,classid)
                try:
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchone()
                        if result == None:
                                return None
                        return CloneClass(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8])
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close()
        '''
        获取所有的克隆群简便信息（version、classid）
        '''
        def selectAllCloneClass(self):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_select = 'select version, classid from cloneclass'
                try:
                        cursor.execute(sql_select)
                        conn.commit()
                        result = cursor.fetchall()
                        return result
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close()                  
                        
                        
class CloneClassMapDao(object):
        def __init__(self):
                pass
        '''
        批量插入克隆群映射
        '''
        def batchInsertCloneClassMap(self, cloneclassmaplist):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_insert = 'insert into cloneclassmap(version, classid, mapversion, mapclassid, similarity, confirm) values(%s, %s, %s, %s, %s, %s)'
                sql_list = []
                for cloneclassmap in cloneclassmaplist:
                        sql_list.append( (cloneclassmap.version, cloneclassmap.classid, cloneclassmap.mapversion, cloneclassmap.mapclassid, cloneclassmap.similarity, cloneclassmap.confirm))
                try:
                        cursor.executemany(sql_insert, sql_list)
                        conn.commit()
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close() 
        '''
        根据version、mapversion获取所有的cloneclassmap对象
        version, classid, mapversion, mapclassid, similarity, confirm
        '''
        def getCloneClassMapList(self, version, mapversion,confirm='yes'):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_select = 'select version, classid, mapversion, mapclassid, similarity, confirm from cloneclassmap where version=%s and mapversion=%s and confirm=%s'
                sql_tuple = (version,mapversion,confirm)
                try:
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchall()
                        cloneclassmap_list = []
                        for one in result:
                                cloneclassmap_list.append(CloneClassMap(one[0], one[1], one[2], one[3], one[4], one[5]))
                        return cloneclassmap_list
                        
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close()
                        
        '''
        使用后继获得前驱列表(version，classid)
        '''
        def getPrecursorListUseSuccessor(self, mapversion, mapclassid, confirm='yes'):
#                 s5 = time.time()
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
#                 e5 = time.time()
#                 print '获取连接花费时间 ： %s'  % (e5 - s5)
                sql_select = 'select version, classid from cloneclassmap where mapversion=%s and mapclassid=%s and confirm=%s'
                sql_tuple = (mapversion, mapclassid, confirm)
                try:
#                         s5 = time.time()
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchall()
#                         e5 = time.time()
#                         print 'sql语句花费时间 ： %s'  % (e5 - s5)
                        precursorlist = []
                        for one in result:
                                precursor = (one[0], one[1])
                                precursorlist.append(precursor)
                        #print 'len(result)',result
                        return precursorlist
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
#                         s5 = time.time()
                        cursor.close()
                        conn.close()     
#                         e5 = time.time()
#                         print '关闭连接花费时间 ： %s'  % (e5 - s5)
    
        '''
        使用前驱获得后继列表(mapversion，mapclassid)
        '''
        def getSuccessorListUsePrecursor(self, version, classid, confirm='yes'):
#                 s3 = time.time()
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
#                 e3 = time.time()
#                 print '获取连接花费时间 ： %s' % (e3 - s3)
                sql_select = 'select mapversion, mapclassid from cloneclassmap where version=%s and classid=%s and confirm=%s'
                sql_tuple = (version, classid, confirm)
                try:
#                         s3 = time.time()
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchall()
#                         e3 = time.time()
#                         print 'sql语句花费时间 ： %s' % (e3 - s3)
                        successorlist = []
                        for one in result:
                                successor = (one[0], one[1])
                                successorlist.append(successor)
                        #print 'len(result)', result
                        return successorlist
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
#                         s3 = time.time()
                        cursor.close()
                        conn.close()
#                         e3 = time.time()
#                         print '关闭连接花费时间 ： %s' % (e3 - s3)

        '''
        统计某个克隆群在图中的度
        '''
        def getDegreeOfCloneClass(self, version, classid, confirm='yes'):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_select = 'select count(*) from cloneclassmap where (version=%s and classid=%s or mapversion=%s and mapclassid=%s) and confirm=%s'
                sql_tuple = (version, classid, version, classid, confirm)
                try:
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchone()
                        return result[0]
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close()
                        

class CloneFragmentMapDao(object):
        def __init__(self):
                pass
        '''
        批量插入克隆片段映射
        '''
        def batchInsertCloneFragmentMap(self, clonefragmentmaplist):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_insert = 'insert into clonefragmentmap(version, pcid, mapversion, mappcid, similarity) values(%s, %s, %s, %s, %s)'
                sql_list = []
                for clonefragmentmap in clonefragmentmaplist:
                        sql_list.append( (clonefragmentmap.version, clonefragmentmap.pcid, clonefragmentmap.mapversion, clonefragmentmap.mappcid, clonefragmentmap.similarity))
                try:
                        cursor.executemany(sql_insert, sql_list)
                        conn.commit()
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close() 
                        
        '''
        根据version、mapversion获得相邻版本的所有克隆片段映射对象
        '''
        def getCloneFragmentMapList(self, version, mapversion):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_select = 'select version, pcid, mapversion, mappcid, similarity from clonefragmentmap where version=%s and mapversion=%s'
                sql_tuple = (version,mapversion)
                try:
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchall()
                        clonefragmentmap_list = []
                        for one in result:
                                clonefragmentmap_list.append(CloneFragmentMap(one[0], one[1], one[2], one[3], one[4]))
                        return clonefragmentmap_list
                        
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close()


class CloneClassShortEvolvePatternDao(object):
        def __init__(self):
                pass
        '''
        批量插入克隆群短期演化模式
        '''
        def batchInsertCloneClassShortEvolvePattern(self, cloneclassshortevolvepatternlist):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_insert = 'insert into cloneclassshortevolvepattern(version, classid, cloneclasslabel, clonefragmentlabel, contentlabel, ismodify, isbug, clonegenealogyid) values(%s, %s, %s, %s, %s, %s, %s, %s)'
                sql_list = []
                for cloneclassshortevolvepattern in cloneclassshortevolvepatternlist:
                        sql_list.append( (cloneclassshortevolvepattern.version, cloneclassshortevolvepattern.classid, cloneclassshortevolvepattern.cloneclasslabel, cloneclassshortevolvepattern.clonefragmentlabel, cloneclassshortevolvepattern.contentlabel, cloneclassshortevolvepattern.ismodify, cloneclassshortevolvepattern.isbug, cloneclassshortevolvepattern.clonegenealogyid))
                try:
                        cursor.executemany(sql_insert, sql_list)
                        conn.commit()
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close() 
                        
        '''
        根据version，clonegenealogyid=''，获取一个克隆谱系的新引子
        '''
        def getOneNewCloneClassShortEvolvePattern(self, version, clonegenealogyid=''):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_select = 'select version, classid, cloneclasslabel, clonefragmentlabel, contentlabel, ismodify, isbug, clonegenealogyid from cloneclassshortevolvepattern where version=%s and clonegenealogyid=%s'
                sql_tuple = (version,clonegenealogyid)
                try:
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchone()
                        if result == None:
                                return None
                        return CloneClassShortEvolvePattern(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close()
        
        '''
        根据version、classid返回克隆群短期演化模式对象
        '''  
        def getCloneClassShortEvolvePattern(self, version, classid):
#                 s4 = time.time()
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
#                 e4 = time.time()
#                 print '获取连接花费时间 ： %s'  % (e4 - s4)
                sql_select = 'select version, classid, cloneclasslabel, clonefragmentlabel, contentlabel, ismodify, isbug, clonegenealogyid from cloneclassshortevolvepattern where version=%s and classid=%s'
                sql_tuple = (version, classid)
                try:
#                         s4 = time.time()
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchone()
#                         e4 = time.time()
#                         print 'sql语句花费时间 ： %s'  % (e4 - s4)
                        if result != None:
                                cloneclassshortevolvepattern = CloneClassShortEvolvePattern(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
                                return cloneclassshortevolvepattern
                        else:
                                return None
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
#                         s4 = time.time()
                        cursor.close()
                        conn.close()    
#                         e4 = time.time()
#                         print '关闭连接花费时间 ： %s'  % (e4 - s4)
        
        '''
        根据version、classid批量更新clonegenealogyid
        '''
        def batchUpdateCloneClassShortEvolvePattern(self, cloneclassshortevolvepatternlist):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_insert = 'update cloneclassshortevolvepattern set clonegenealogyid=%s where version=%s and classid=%s'
                sql_list = []
                for cloneclassshortevolvepattern in cloneclassshortevolvepatternlist:
                        sql_list.append( (cloneclassshortevolvepattern.clonegenealogyid, cloneclassshortevolvepattern.version, cloneclassshortevolvepattern.classid))
                try:
                        cursor.executemany(sql_insert, sql_list)
                        conn.commit()
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close() 
        
        '''
        更新一个克隆群的克隆谱系编号字段
        '''
        def updateOneCloneClassShortEvolvePattern(self, cloneclassshortevolvepattern):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_insert = 'update cloneclassshortevolvepattern set clonegenealogyid=%s where version=%s and classid=%s'
                sql_tuple = (cloneclassshortevolvepattern.clonegenealogyid, cloneclassshortevolvepattern.version, cloneclassshortevolvepattern.classid)
                try:
                        cursor.execute(sql_insert, sql_tuple)
                        conn.commit()
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close() 
                        
                        
        '''
        获取某个克隆谱系包含的所有克隆群（克隆群短期演化模式）
        '''
        def getAllCloneClassShortEvolvePatternForCloneGenealogyId(self, clonegenealogyid):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_select = 'select version, classid, cloneclasslabel, clonefragmentlabel, contentlabel, ismodify, isbug, clonegenealogyid from cloneclassshortevolvepattern where clonegenealogyid=%s'
                sql_tuple = (clonegenealogyid,)
                try:
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchall()
                        cloneclassshortevolvepatternlist = []
                        for one in result:
                                cloneclassshortevolvepattern = CloneClassShortEvolvePattern(one[0], one[1], one[2], one[3], one[4], one[5], one[6], one[7])
                                cloneclassshortevolvepatternlist.append(cloneclassshortevolvepattern)
                        return cloneclassshortevolvepatternlist
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close()    
        
        #以cloneclasslabel为视角统计各演化模式克隆群数量
        def statisticalNumberByCloneClassLabel(self, cloneclasslabel, ismodify=None, isbug=None):
                if ismodify not in [None, 'yes']:
                        return -1
                if isbug not in [None, 'yes']:
                        return -1
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_select, sql_tuple = None, None
                if ismodify == None and isbug == None:
                        sql_select = 'select count(*) from cloneclassshortevolvepattern where cloneclasslabel=%s'
                        sql_tuple = (cloneclasslabel,)
                if ismodify == 'yes' and isbug == None:
                        sql_select = 'select count(*) from cloneclassshortevolvepattern where cloneclasslabel=%s and ismodify=%s'
                        sql_tuple = (cloneclasslabel,'yes')
                if ismodify == 'yes' and isbug == 'yes':
                        sql_select = 'select count(*) from cloneclassshortevolvepattern where cloneclasslabel=%s and ismodify=%s and isbug=%s'
                        sql_tuple = (cloneclasslabel,'yes', 'yes')
                try:
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchone()
                        return result[0]
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close()    
        
        #以clonefragmentlabel为视角统计各演化模式克隆群数量
        def statisticalNumberByCloneFragmentLabel(self, clonefragmentlabel, ismodify=None, isbug=None):
                if ismodify not in [None, 'yes']:
                        return -1
                if isbug not in [None, 'yes']:
                        return -1
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_select, sql_tuple = None, None
                if ismodify == None and isbug == None:
                        sql_select = 'select count(*) from cloneclassshortevolvepattern where clonefragmentlabel=%s'
                        sql_tuple = (clonefragmentlabel,)
                if ismodify == 'yes' and isbug == None:
                        sql_select = 'select count(*) from cloneclassshortevolvepattern where clonefragmentlabel=%s and ismodify=%s'
                        sql_tuple = (clonefragmentlabel,'yes')
                if ismodify == 'yes' and isbug == 'yes':
                        sql_select = 'select count(*) from cloneclassshortevolvepattern where clonefragmentlabel=%s and ismodify=%s and isbug=%s'
                        sql_tuple = (clonefragmentlabel,'yes', 'yes')
                try:
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchone()
                        return result[0]
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close()    
                        
        #以contentlabel为视角统计各演化模式克隆群数量
        def statisticalNumberByContentLabel(self, contentlabel, ismodify=None, isbug=None):
                if ismodify not in [None, 'yes']:
                        return -1
                if isbug not in [None, 'yes']:
                        return -1
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_select, sql_tuple = None, None
                if ismodify == None and isbug == None:
                        sql_select = 'select count(*) from cloneclassshortevolvepattern where contentlabel=%s'
                        sql_tuple = (contentlabel,)
                if ismodify == 'yes' and isbug == None:
                        sql_select = 'select count(*) from cloneclassshortevolvepattern where contentlabel=%s and ismodify=%s'
                        sql_tuple = (contentlabel,'yes')
                if ismodify == 'yes' and isbug == 'yes':
                        sql_select = 'select count(*) from cloneclassshortevolvepattern where contentlabel=%s and ismodify=%s and isbug=%s'
                        sql_tuple = (contentlabel,'yes', 'yes')
                try:
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchone()
                        return result[0]
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close()    
        
class CloneGenealogyDao(object):
        def __init__(self):
                pass
        
        '''
        插入一条克隆谱系信息
        '''
        def insertOneCloneGenealogy(self, clonegenealogy):
#                 print clonegenealogy.longevolvepattern
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
#                 print 
                sql_insert = 'insert into clonegenealogy(software, clonegenealogyid, deathnumber, grownnumber, separatenumber, mergenumber, complexnumber, pendingnumber, longevolvepattern, keepnumber, deletenumber, addnumber, deleteandaddnumber, nochangenumber, consistentnumber, inconsistentnumber, undergoversions, undergoversionnumber, ismodify, isbug) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                sql_tuple = (clonegenealogy.software, clonegenealogy.clonegenealogyid, clonegenealogy.deathnumber, clonegenealogy.grownnumber, clonegenealogy.separatenumber, clonegenealogy.mergenumber, clonegenealogy.complexnumber, clonegenealogy.pendingnumber, clonegenealogy.longevolvepattern, clonegenealogy.keepnumber, clonegenealogy.deletenumber, clonegenealogy.addnumber, clonegenealogy.deleteandaddnumber, clonegenealogy.nochangenumber, clonegenealogy.consistentnumber, clonegenealogy.inconsistentnumber, clonegenealogy.undergoversions, clonegenealogy.undergoversionnumber, clonegenealogy.ismodify, clonegenealogy.isbug)
                try:
                        cursor.execute(sql_insert, sql_tuple)
                        conn.commit()
                        #print '插入成功！！！'
                except Exception as e:
                        conn.rollback()
                        print e
                        #print '插入失败！！！'
                finally:
                        cursor.close()
                        conn.close()
        
        '''
        提取某个软件的所有克隆谱系
        '''
        def selectAllCloneGenealogyForSoftware(self, software):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_select = 'select software, clonegenealogyid, deathnumber, grownnumber, separatenumber, mergenumber, complexnumber, pendingnumber, longevolvepattern, keepnumber, deletenumber, addnumber, deleteandaddnumber, nochangenumber, consistentnumber, inconsistentnumber, undergoversions, undergoversionnumber, ismodify, isbug from clonegenealogy where software = %s'
                sql_tuple = (software,)
                try:
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchall()
                        clonegenealogylist = []
                        for one in result:
                                clonegenealogy = CloneGenealogy(one[0], one[1], one[2], one[3], one[4], one[5], one[6], one[7], one[8], one[9], one[10], one[11], one[12], one[13], one[14], one[15], one[16], one[17], one[18], one[19])
                                clonegenealogylist.append(clonegenealogy)
                        return clonegenealogylist
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close()
        
        '''
        批量更新克隆谱系（longevolvepattern）
        '''
        def batchUpdateCloneGenealogyForLongEvolvePattern(self, clonegenealogylist):
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_insert = 'update clonegenealogy set longevolvepattern=%s where software=%s and clonegenealogyid=%s'
                sql_list = []
                for clonegenealogy in clonegenealogylist:
                        sql_list.append( (clonegenealogy.longevolvepattern, clonegenealogy.software, clonegenealogy.clonegenealogyid))
                try:
                        cursor.executemany(sql_insert, sql_list)
                        conn.commit()
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close() 
                        
        #统计各演化模式的克隆谱系数量
        def statisticalNumberByLongevolvePattern(self, longevolvepattern, ismodify=None, isbug=None):
                if ismodify not in [None, 'yes']:
                        return -1
                if isbug not in [None, 'yes']:
                        return -1
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_select, sql_tuple = None, None
                if ismodify == None and isbug == None:
                        sql_select = 'select count(*) from clonegenealogy where longevolvepattern=%s'
                        sql_tuple = (longevolvepattern,)
                if ismodify == 'yes' and isbug == None:
                        sql_select = 'select count(*) from clonegenealogy where longevolvepattern=%s and ismodify>0'
                        sql_tuple = (longevolvepattern,)
                if ismodify == 'yes' and isbug == 'yes':
                        sql_select = 'select count(*) from clonegenealogy where longevolvepattern=%s and ismodify>0 and isbug>0'
                        sql_tuple = (longevolvepattern,)
                try:
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchone()
                        return result[0]
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close()    
        
        #统计各演化模式克隆谱系包含的克隆群数
        def statisticalCloneClassNumberByLongevolvePattern(self, longevolvepattern, ismodify=None, isbug=None):
                if ismodify not in [None, 'yes']:
                        return -1
                if isbug not in [None, 'yes']:
                        return -1
                conn = DBmanager.getDBConnect()
                cursor = conn.cursor()
                sql_select, sql_tuple = None, None
                if ismodify == None and isbug == None:
                        sql_select = 'select sum(nochangenumber+consistentnumber+inconsistentnumber+pendingnumber) from clonegenealogy  where longevolvepattern=%s'
                        sql_tuple = (longevolvepattern,)
                if ismodify == 'yes' and isbug == None:
                        sql_select = 'select sum(ismodify) from clonegenealogy where longevolvepattern=%s'
                        sql_tuple = (longevolvepattern,)
                if ismodify == 'yes' and isbug == 'yes':
                        sql_select = 'select sum(isbug) from clonegenealogy where longevolvepattern=%s'
                        sql_tuple = (longevolvepattern,)
                try:
                        cursor.execute(sql_select, sql_tuple)
                        conn.commit()
                        result = cursor.fetchone()
                        return result[0]
                except Exception as e:
                        conn.rollback()
                        print e
                finally:
                        cursor.close()
                        conn.close()    