#coding=utf-8
from dao import *
from ggstools import *
import os.path

'''
分角度统计各演化模式克隆群数量
'''
def evolveCount(software, workhome):
        cloneclasslabellist = ['death', 'grown', 'separate', 'merge', 'complex', 'pending']
        clonefragmentlabellist = ['delete', 'add', 'keep', 'delete add', 'pending']
        contentlabellist = ['nochange', 'consistent', 'inconsistent', 'pending']
        cloneclassshortevolvepatternDao = CloneClassShortEvolvePatternDao()
        resultpath = os.path.join(workhome, software + '.result')
        fw = open(resultpath, 'w')
        fw.write('software : %s\n' % software)
        
        #统计cloneclasslabel各短期演化模式数量
        fw.write('\n')
        fw.write('cloneclasslabel\n')
        fw.write('---------------------------\n')
        for cloneclasslabel in cloneclasslabellist:
                totalnumber = cloneclassshortevolvepatternDao.statisticalNumberByCloneClassLabel(cloneclasslabel)
                modifynumber = cloneclassshortevolvepatternDao.statisticalNumberByCloneClassLabel(cloneclasslabel, 'yes')
                bugnumber = cloneclassshortevolvepatternDao.statisticalNumberByCloneClassLabel(cloneclasslabel, 'yes', 'yes')
                fw.write('cloneclasslabel : %s\n' % cloneclasslabel)
                fw.write('totalnumber : %s\n' % totalnumber)
                fw.write('modifynumber : %s\n' % modifynumber)
                fw.write('bugnumber : %s\n' % bugnumber)
                fw.write('---------------------------\n')
                #print totalnumber, modifynumber, bugnumber
        fw.flush()
        
        #统计clonefragmentlabel各短期演化模式数量
        fw.write('\n')
        fw.write('clonefragmentlabel\n')
        fw.write('---------------------------\n')
        for clonefragmentlabel in clonefragmentlabellist:
                totalnumber = cloneclassshortevolvepatternDao.statisticalNumberByCloneFragmentLabel(clonefragmentlabel)
                modifynumber = cloneclassshortevolvepatternDao.statisticalNumberByCloneFragmentLabel(clonefragmentlabel, 'yes')
                bugnumber = cloneclassshortevolvepatternDao.statisticalNumberByCloneFragmentLabel(clonefragmentlabel, 'yes', 'yes')
                fw.write('clonefragmentlabel : %s\n' % clonefragmentlabel)
                fw.write('totalnumber : %s\n' % totalnumber)
                fw.write('modifynumber : %s\n' % modifynumber)
                fw.write('bugnumber : %s\n' % bugnumber)
                fw.write('---------------------------\n')
                #print totalnumber, modifynumber, bugnumber
        fw.flush()
        
        #统计contentlabel各短期演化模式数量
        fw.write('\n')
        fw.write('contentlabel\n')
        fw.write('---------------------------\n')
        for contentlabel in contentlabellist:
                totalnumber = cloneclassshortevolvepatternDao.statisticalNumberByContentLabel(contentlabel)
                modifynumber = cloneclassshortevolvepatternDao.statisticalNumberByContentLabel(contentlabel, 'yes')
                bugnumber = cloneclassshortevolvepatternDao.statisticalNumberByContentLabel(contentlabel, 'yes', 'yes')
                fw.write('contentlabel : %s\n' % contentlabel)
                fw.write('totalnumber : %s\n'  % totalnumber)
                fw.write('modifynumber : %s\n' % modifynumber)
                fw.write('bugnumber : %s\n'  % bugnumber)
                fw.write('---------------------------\n')
                #print totalnumber, modifynumber, bugnumber
        fw.flush()
        
        #统计长期演化模式数量
        longevolvepatternlist = ['mixture', 'general', 'independent', 'merge', 'reconsolidation', 'freedom']
        fw.write('\n')
        fw.write('longevolvepattern\n')
        fw.write('---------------------------\n')
        clonegenealogyDao = CloneGenealogyDao()
        for longevolvepattern in longevolvepatternlist:
                totalnumber = clonegenealogyDao.statisticalNumberByLongevolvePattern(longevolvepattern)
                modifynumber = clonegenealogyDao.statisticalNumberByLongevolvePattern(longevolvepattern, 'yes')
                bugnumber = clonegenealogyDao.statisticalNumberByLongevolvePattern(longevolvepattern, 'yes', 'yes')
                fw.write('longevolvepattern : %s\n' % longevolvepattern)
                fw.write('totalnumber : %s\n'  % totalnumber)
                fw.write('modifynumber : %s\n' % modifynumber)
                fw.write('bugnumber : %s\n'  % bugnumber)
                fw.write('---------------------------\n')
                #print totalnumber, modifynumber, bugnumber
        fw.flush()
        
        #统计各类克隆家系包含的克隆群数
        fw.write('\n')
        fw.write('longevolvepattern  for cloneclass\n')
        fw.write('---------------------------\n')
        clonegenealogyDao = CloneGenealogyDao()
        for longevolvepattern in longevolvepatternlist:
                totalcloneclassnumber = clonegenealogyDao.statisticalCloneClassNumberByLongevolvePattern(longevolvepattern)
                modifycloneclassnumber = clonegenealogyDao.statisticalCloneClassNumberByLongevolvePattern(longevolvepattern, 'yes')
                bugcloneclassnumber = clonegenealogyDao.statisticalCloneClassNumberByLongevolvePattern(longevolvepattern, 'yes', 'yes')
                fw.write('longevolvepattern : %s\n' % longevolvepattern)
                fw.write('totalcloneclassnumber : %s\n'  % totalcloneclassnumber)
                fw.write('modifycloneclassnumber : %s\n' % modifycloneclassnumber)
                fw.write('bugcloneclassnumber : %s\n'  % bugcloneclassnumber)
                fw.write('---------------------------\n')
        fw.flush()
        fw.close()

def main(software, ip, workhome):
        evolveCount(software, workhome)
        subject = '%s @  %s' % (software, ip)
        content = 'result OK'
        mailAlert(subject, content)


# if __name__ == '__main__':
#         #设置区域
#         keyvaluedict = readConfig()
#         software = keyvaluedict['software']
#         ip = keyvaluedict['ip']
#         workhome = keyvaluedict['workhome']
#         #设置区域
#         main(software, ip, workhome)

        