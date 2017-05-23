#coding=utf-8
import os
import re
import time
import shutil
import logging
import os.path
import xml.sax
from dao import *
from handler import *
from ggstools import *
    
'''
将masterpath目录下所有源码（除git相关文件）拷贝到destinationpath目录下
'''
def copyVersionDirectory(masterpath, destinationpath):
        files = os.listdir(masterpath)
        for file in files:
                if file.startswith('.git'):#git相关文件忽略
                        continue
                filepath = os.path.join(masterpath, file)
                if os.path.isdir(filepath):
                        shutil.copytree(filepath, os.path.join(destinationpath,file))
                if os.path.isfile(filepath):
                        shutil.copyfile(filepath, os.path.join(destinationpath,file))
                        
'''
对一个版本的源码进行克隆检测
NiCad granularity language systems/systemdir [ config ]
          where granularity is one of:  { functions blocks ... }
          and   language    is one of:  { c java cs py ... }
          and   config      is one of:  { blindrename ... }
'''
def checkCloneCode(nicadpath, sourcepath, language, granularity):
        os.chdir(nicadpath)
        check_clone_cmd = './nicad4 %s %s %s 1>/dev/null 2>&1' % (granularity, language, sourcepath)
        logging.info('cmd : %s' % check_clone_cmd)
        result = os.system(check_clone_cmd)
        if result != 0:
                logging.debug('%s  fail' % check_clone_cmd)
                return False
        else:
                logging.info('%s success' % check_clone_cmd)
                return True
        
'''
导出一个版本的源码，并返回拷贝的目的地路径
2c90bd796dbaa09fe8ec3be9aa66293d5f4156ba
'''
def exportOneVersionSource(gitcodepath, software, commitid, tmppath):
        #获得软件的git主目录
        masterpath = os.path.join(gitcodepath, software)
        #使用git reset命令，将版本回退到commitid版本
        os.chdir(masterpath)
        git_reset_cmd = 'git reset --hard %s 1>/dev/null 2>&1' % commitid
        result = os.system(git_reset_cmd)
        if result == 0:
                logging.info('%s reset success' % commitid)
        else:
                logging.debug('%s reset fail' % commitid)
                return False
        #准备克隆检测场所
        if not os.path.isdir(tmppath):
                os.mkdir(tmppath)
        check_clone_code = os.path.join(tmppath, 'check_clone_code')
        if os.path.exists(check_clone_code):
                shutil.rmtree(check_clone_code)
        os.mkdir(check_clone_code)
        sourcepath = os.path.join(check_clone_code, 'source')
        os.mkdir(sourcepath)
        copyVersionDirectory(masterpath, sourcepath)
        return sourcepath
        


'''
<source file="/home/servlet/MultipartConfigElement.java" startline="32" endline="42">
......
</source>
'''
def pretreatmentCloneFragmentXML(filepath):
        fr_old = open(filepath, 'r')
        new_filepath = filepath + '.new'
        fw_new = open(new_filepath, 'w')
        fw_new.write('<sources>\n') #先写个根
        for line in fr_old.readlines():
                #乱码数据不能解析的情况下，直接替换整行数据
                if 'if (Character.isLetterOrDigit ((char) c)' in line:
                        line = 'if (Character.isLetterOrDigit ((char) c) || ((c != \'#\') && (c != \'{\') && (c != \'}\') && (c != \' \') && (c != \'~\') && (c != \' \') && (c != \',\'))) {'
                elif 'LANGUAGES.put (' in line:
                        line = 'LANGUAGES.put (" ", " ");'
                elif 'HTML_CHARS.put (' in line:
                        line = 'HTML_CHARS.put (" ", " ");'
                elif 'assertEquals (' in line:
                        line = 'assertEquals (" ", " ");'
                elif 'rdf:Description rdf:about' in line:
                        line = 'return x'
                elif 'e.setField' in line:
                        line = 'e.setField(" ", " ")'
                elif 'String bibtex' in  line:
                        line = 'String bibtex x'
                elif 'bibtex:abstract' in line:
                        line = 'bibtex:abstract'
                elif 'assertNameFormatA' in line:
                        line = 'assertNameFormatA'
                elif 'assertNameFormatB' in line:
                        line = 'assertNameFormatB'
                elif 'assertNameFormatC' in line:
                        line = 'assertNameFormatC'
                elif 'XML_CHARS.put' in line:
                        line = 'XML_CHARS.put(" ", " ")'
                elif 'if (ke.getKeyChar () == ' in line:
                        line = 'if (ke.getKeyChar () == ' ') {'
                        
                        
                line = line.replace(']]>', '   ')#如果有xml解析出问题的字符，直接在这里替换掉
                if line.startswith('<source file='):
                        fw_new.write(line)
                        fw_new.write('<![CDATA[')
                elif line.startswith('</source>'):
                        fw_new.write(']]>')
                        fw_new.write(line)
                else:
                        fw_new.write(line)
                fw_new.flush()

        fw_new.write('</sources>')
        fw_new.close()
        fr_old.close()
        os.remove(filepath)
        os.rename(new_filepath, filepath)

'''
将克隆片段导入数据库
'''  
def importCloneFragmentToDB(version, filepath, prefixlen):
        #克隆片段文件不可xml解析，先预处理
        pretreatmentCloneFragmentXML(filepath)
        #第一步：使用parser对存放克隆片段源码的xml文件进行解析
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        Handler = CloneFragmentHandler(version)
        parser.setContentHandler(Handler)
        parser.parse(filepath)
        clonefragmentlist = Handler.clonefragmentlist
        
        #处理file字符，去掉前缀
        for i in range(len(clonefragmentlist)):
                clonefragmentlist[i].file = clonefragmentlist[i].file[prefixlen:]
                #如果后缀是'.ifdefed'，去掉
                if clonefragmentlist[i].file.endswith('.ifdefed'):
                        clonefragmentlist[i].file = clonefragmentlist[i].file[:-1*len('.ifdefed')]
                
        #第二步：将解析出来的clonefragment放入数据库中
        clonefragmentDao = CloneFragmentDao()
        clonefragmentDao.batchInsertCloneFragment(clonefragmentlist)
        logging.info('version : %s , clonefragment save to database' % version)
        
        clonefragmentnumber = len(clonefragmentlist)
        #为了方便克隆群topic生成，准备一个克隆片段字典，key=pcid，value=source
        clonefragmentdict = {}
        for clonefragment in clonefragmentlist:
                clonefragmentdict[int(clonefragment.pcid)] = clonefragment.source
        return clonefragmentdict, clonefragmentnumber

# # '''
# # 使用克隆群的一个片段内容代替克隆群
# # '''
# # def getTopicFromCloneFragmentSet(pcidset, clonefragmentdict):
# #         return clonefragmentdict[int(pcidset[0])]
# '''
# 根据pcidset获取克隆群主题
# clonefragmentdict {'1':'aaaaa'}
# '''
# def getTopicFromCloneFragmentSet(pcidset, clonefragmentdict):
#         #定义分隔符
#         splitword = '|'.join([' ','\t','\n','\(','\)','\[','\]','\{','\}','<','>','=','&','!','\|','\.',';',':','\?','\"','\'','\+','\*',',',';','-','/','0','1','2','3','4','5','6','7','8','9'])
#         #定义停用词
#         stopword = ['','int','char','bool','float','double','if','else','switch','case','for','while','do','break','continue','return','CDATA','static','public','new','byte']
#         #分割每一个克隆片段，将单词放入字典
#         word_dict = {}
#         pcidlist = pcidset.split('-')
#         for pcid in pcidlist:
#                 words = re.split(splitword, clonefragmentdict[int(pcid)])
#                 for word in words:
#                         word_dict[word] = word_dict.get(word,  0) + 1
#         #对单词，按照词频排序
#         word_list = []
#         for word in word_dict.keys():
#                 if word not in stopword:
#                         word_list.append((word, word_dict[word]))
#                          
#         word_list.sort(key=lambda x:(x[1],x[0]), reverse=True)
#         #生成主题
#         topic = []
#         number = 10
#         for word in word_list:
#                 number = number - 1
#                 topic.append(word[0])
#                 if number == 0:
#                         break
#         return ' '.join(topic)                
                
'''
将克隆群导入数据库
'''
def importCloneClassToDB(version, filepath, clonefragmentdict):
        #第一步：使用parser对存放克隆群的xml文件进行解析
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        Handler = CloneClassHandler(version)
        parser.setContentHandler(Handler)
        parser.parse(filepath)
        cloneclasslist = Handler.cloneclasslist
        
#         #更新topic字段
#         for i in range(len(cloneclasslist)):
#                 cloneclasslist[i].topic = getTopicFromCloneFragmentSet(cloneclasslist[i].pcidset, clonefragmentdict)
                
        #第二步：将解析出来的cloneclass放入数据库中
        cloneclassDao = CloneClassDao()
        cloneclassDao.batchInsertCloneClass(cloneclasslist)
        logging.info('version : %s, cloneclass save to database'  % version)
        cloneclassnumber = len(cloneclasslist)    
        return cloneclassnumber

'''
对某个软件所有版本进行克隆检测
首先获取该版本的源码，然后进行克隆检测，最后将检测结果(已经更新克隆群topic字段)批量导入数据库
'''
def cloneCheckForSoftware(software, subject, language, granularity, threshold, rename, gitcodepath, tmppath, nicadpath,to_addr):
        #获取所有的版本信息
        versioninfoDao = VersionInfoDao()
        versioninfolist = versioninfoDao.selectAllVersionInfoForSoftware(software)
        for i  in range(len(versioninfolist)):
                #如果中间版本克隆检测失败，从新在这里开始
                if versioninfolist[i].cloneclassnumber not in ['', '0']:
                        continue
                logging.info('------------------------------------------------------------------------')
                logging.info('begin clone check    [%s]' % versioninfolist[i].version)
                start = time.time()
                #获取版本源码，拷贝到指定路径sourcepath
                logging.info('get source ...' )
                sourcepath = exportOneVersionSource(gitcodepath, software, versioninfolist[i].commitid, tmppath)
                #说明： 以下两处直接跳过部分，正常实验，不应该如此，但源代码或者nicad确实存在异常情况，不得已而为之
                #如果获取源码失败，直接跳过去
                if sourcepath == False:
                        versioninfolist[i].cloneclassnumber = 0
                        versioninfolist[i].clonefragmentnumber = 0
                        versioninfoDao.updateNumberForVersion(versioninfolist[i])
                        logging.info('get source fail')
                        logging.info('-------------------------------------------------------------')
                        mailAlert(subject, '[%s] get source fail' % versioninfolist[i].version,to_addr)
                        continue
                
                logging.info('get source success' )
                #对该版本的代码进行克隆检测
                logging.info('nicad run  ...' )
                nicadresult = checkCloneCode(nicadpath, sourcepath, language, granularity)
                logging.info('nicad run  over' )
                #如果克隆检测出现问题，那么直接跳过去
                if nicadresult == False:
                        versioninfolist[i].cloneclassnumber = 0
                        versioninfolist[i].clonefragmentnumber = 0
                        versioninfoDao.updateNumberForVersion(versioninfolist[i])
                        logging.info('clone check fail')
                        logging.info('-------------------------------------------------------------')
                        mailAlert(subject, '[%s] clone check fail' % versioninfolist[i].version,to_addr)
                        continue
                        
                #将克隆检测结果导入数据库
                clonefragmentfilepath = os.path.join(tmppath, 'check_clone_code' ,'source_%s.xml' % granularity)
                cloneclassfilepath = os.path.join(tmppath, 'check_clone_code' ,'source_%s%s-clones' % (granularity, rename), 'source_%s%s-clones-%s-classes.xml' % (granularity, rename,threshold))
                #导入克隆片段，并返回克隆片段字典 1:source
                #len('/home/geguangshuai/workspace/CodeClone/tmp/check_clone_code/source')
                prefixlen = len(sourcepath)
                clonefragmentdict, clonefragmentnumber = importCloneFragmentToDB(versioninfolist[i].version, clonefragmentfilepath, prefixlen)
                #导入克隆群
                cloneclassnumber = importCloneClassToDB(versioninfolist[i].version, cloneclassfilepath, clonefragmentdict)
                
                #更新克隆群、克隆片段数量字段
                versioninfolist[i].cloneclassnumber = cloneclassnumber
                versioninfolist[i].clonefragmentnumber = clonefragmentnumber
                versioninfoDao.updateNumberForVersion(versioninfolist[i])
                
                end = time.time()
                logging.info('clone check cost time ： %s'  % (end - start))
                logging.info('-------------------------------------------------------------')
                
                if (i+1) % 10 == 0:
                        content = '共 %s 个版本， %s 个版本已经完成克隆检测' % (len(versioninfolist), str(i+1))
                        mailAlert(subject, content,to_addr)
        #end for
        return len(versioninfolist)
#         #批量更新克隆群、克隆片段数量
#         versioninfoDao.batchUpdateNumberForSoftware(versioninfolist)
        
                
def main(software, ip, language, granularity, threshold, rename, gitcodepath, tmppath, nicadpath,to_addr):
        logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='%s.log' % software,
                        filemode='a')
        logging.info('start clone detection')
        subject = '%s @  %s' % (software, ip)
        try:
                versionnumber = cloneCheckForSoftware(software, subject, language, granularity, threshold, rename, gitcodepath, tmppath, nicadpath,to_addr)
                content = '所有版本克隆检测完毕，共 %s 个版本' % versionnumber
                logging.info(content)
                mailAlert(subject, content,to_addr)
        except Exception, e:
                content = '克隆检测过程中出现错误'
                logging.info(content)
                mailAlert(subject, content,to_addr)