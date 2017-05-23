#coding=utf-8

'''
一次提交
'''
class Commit(object):
        def __init__(self, software, number, commitdate, commitid, describeinfo, changeinfo, isbugfix):
                self.software, self.number, self.commitdate, self.commitid, self.describeinfo, self.changeinfo, self.isbugfix = software, number, commitdate, commitid, describeinfo, changeinfo, isbugfix

'''
一个版本的克隆群、克隆片段数量信息
'''
class VersionInfo(object):
        def __init__(self, software, version, commitid, cloneclassnumber, clonefragmentnumber, changeinfo='', bugfixinfo=''):
                self.software, self.version, self.commitid, self.cloneclassnumber, self.clonefragmentnumber, self.changeinfo, self.bugfixinfo =  software, version, commitid, cloneclassnumber, clonefragmentnumber, changeinfo, bugfixinfo
        
'''
克隆片段
'''
class CloneFragment(object):
        def __init__(self, version, pcid, file, startline, endline, source, ismodify='', isbug='', maybelocation=''):
                self.version, self.pcid, self.file, self.startline, self.endline, self.source, self.ismodify, self.isbug, self.maybelocation = version, pcid, file, startline, endline, source,  ismodify, isbug, maybelocation
                if self.maybelocation == '':
                        self.maybelocation = self.startline + '+' + self.endline

'''
克隆群
'''
class CloneClass(object):
        def __init__(self, version, classid, nclones, nlines, similarity, pcidset, topic='', ismodify='', isbug=''):
                self.version, self.classid, self.nclones, self.nlines, self.similarity, self.pcidset, self.topic, self.ismodify, self.isbug = version, classid, nclones, nlines, similarity, pcidset, topic, ismodify, isbug
                
'''
克隆群映射
'''
class CloneClassMap(object):
        def __init__(self, version, classid, mapversion, mapclassid, similarity, confirm='yes'):
                self.version, self.classid, self.mapversion, self.mapclassid, self.similarity, self.confirm = version, classid, mapversion, mapclassid, similarity, confirm
                
'''
克隆片段映射
'''
class CloneFragmentMap(object):
        def __init__(self, version, pcid, mapversion, mappcid, similarity):
                self.version, self.pcid, self.mapversion, self.mappcid, self.similarity = version, pcid, mapversion, mappcid, similarity
                
'''
克隆群短期演化模式（cloneclasslabel：克隆群映射个数、clonefragmentlabel：克隆片段变化情况、contentlabel：内容变化情况、ismodify：是否发生了修改、isbug：是否是bug修复）
'''
class CloneClassShortEvolvePattern(object):
        def __init__(self, version, classid, cloneclasslabel, clonefragmentlabel, contentlabel, ismodify='', isbug='', clonegenealogyid=''):
                self.version, self.classid, self.cloneclasslabel, self.clonefragmentlabel, self.contentlabel, self.ismodify, self.isbug, self.clonegenealogyid = version, classid, cloneclasslabel, clonefragmentlabel, contentlabel, ismodify, isbug, clonegenealogyid
                
'''
克隆谱系（software、clonegenealogyid、deathnumber、grownnumber、separatenumber、mergenumber、complexnumber、longevolvepattern、undergoversions、undergoversionnumber、ismodify、isbug）
''' 
class CloneGenealogy(object):
        def __init__(self, software, clonegenealogyid, deathnumber='0', grownnumber='0', separatenumber='0', mergenumber='0', complexnumber='0', pendingnumber='0', longevolvepattern='', keepnumber='0' , deletenumber='0', addnumber='0', deleteandaddnumber='0', nochangenumber='0', consistentnumber='0', inconsistentnumber='0', undergoversions='', undergoversionnumber='', ismodify='0', isbug='0'):
                self.software, self.clonegenealogyid, self.deathnumber, self.grownnumber, self.separatenumber, self.mergenumber, self.complexnumber, self.pendingnumber, self.longevolvepattern, self.keepnumber, self.deletenumber, self.addnumber, self.deleteandaddnumber, self.nochangenumber, self.consistentnumber, self.inconsistentnumber, self.undergoversions, self.undergoversionnumber, self.ismodify, self.isbug = software, clonegenealogyid, deathnumber, grownnumber, separatenumber, mergenumber, complexnumber, pendingnumber, longevolvepattern, keepnumber, deletenumber, addnumber, deleteandaddnumber, nochangenumber, consistentnumber, inconsistentnumber,undergoversions, undergoversionnumber, ismodify, isbug
                self.versionset = set()
                self.undergoversions = u'调用dealwithUndergoVersion即可处理'
        
        #version, classid, cloneclasslabel, clonefragmentlabel, ismodify, isbug, clonegenealogyid
        def addOneCloneClassShortEvolvePattern(self, cloneclassshortevolvepattern):
                #cloneclasslabel
                if cloneclassshortevolvepattern.cloneclasslabel == 'death':
                        self.deathnumber = str(int(self.deathnumber) + 1)
                elif cloneclassshortevolvepattern.cloneclasslabel == 'grown':
                        self.grownnumber = str(int(self.grownnumber) + 1)
                elif cloneclassshortevolvepattern.cloneclasslabel == 'separate':
                        self.separatenumber = str(int(self.separatenumber) + 1)
                elif cloneclassshortevolvepattern.cloneclasslabel == 'merge':
                        self.mergenumber = str(int(self.mergenumber) + 1)
                elif cloneclassshortevolvepattern.cloneclasslabel == 'complex':
                        self.complexnumber = str(int(self.complexnumber) + 1)
                else:
                        self.pendingnumber = str(int(self.pendingnumber) + 1)
                #---------------------------------------------------------------------------------------------------------     
                
                #clonefragmentlabel
                if cloneclassshortevolvepattern.clonefragmentlabel == 'keep':
                        self.keepnumber = str(int(self.keepnumber) + 1)
                elif cloneclassshortevolvepattern.clonefragmentlabel == 'delete':
                        self.deletenumber = str(int(self.deletenumber) + 1)
                elif cloneclassshortevolvepattern.clonefragmentlabel == 'add':
                        self.addnumber = str(int(self.addnumber) + 1)
                #如果该克隆群和下版本的映射，克隆片段即出现了去除又包含新增，一定是“delete add”
                elif cloneclassshortevolvepattern.clonefragmentlabel == 'delete add':
                        self.deleteandaddnumber = str(int(self.deleteandaddnumber) + 1)
                #---------------------------------------------------------------------------------------------------------     
                
                #contentlabel
                if cloneclassshortevolvepattern.contentlabel == 'nochange':
                        self.nochangenumber = str(int(self.nochangenumber) + 1)
                elif cloneclassshortevolvepattern.contentlabel == 'consistent':
                        self.consistentnumber = str(int(self.consistentnumber) + 1)
                elif cloneclassshortevolvepattern.contentlabel == 'inconsistent':
                        self.inconsistentnumber = str(int(self.inconsistentnumber) + 1)
                #---------------------------------------------------------------------------------------------------------     
                
                self.versionset.add(cloneclassshortevolvepattern.version)
                self.undergoversionnumber = str(len(self.versionset))
#                 print cloneclassshortevolvepattern.version, cloneclassshortevolvepattern.classid
                if cloneclassshortevolvepattern.ismodify == 'yes':
                        self.ismodify = str(int(self.ismodify) + 1)
                if cloneclassshortevolvepattern.isbug == 'yes':
                        self.isbug = str(int(self.isbug) + 1)
        
        #目前先不使用，考虑如何对版本排序，可以搞一个list存放所有的版本，排序之后再插入，或者干脆直接放乱序的
        def dealwithUndergoVersion(self):
                 self.undergoversions = list(self.versionset)
                 self.undergoversionnumber = str(len(self.versionset))
                
                
                
                