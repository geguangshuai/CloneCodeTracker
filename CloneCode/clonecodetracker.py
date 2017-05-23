#coding=utf-8
import step1conggithubhuoquyuanmaku
import step2gitloghuoqurizhixinxi
import step3xuanqushiyuanbanben
import step4kelongjiance
import step5gengxinziduan
import step6kelongyingse
import step7tianjiayanhumoshi
import step8tiqukelongpuxibingshibieyanhuamoshi
import step9shujutongji
import ggstools
import os
import os.path
import time


if __name__ == '__main__':
        keyvaluedict = ggstools.readConfig()
        
        software = keyvaluedict['software']
        ip = keyvaluedict['ip']
        language = keyvaluedict['language']
        workhome = keyvaluedict['workhome']
        nicadpath = keyvaluedict['nicadpath']
        start = keyvaluedict['start']
        end = keyvaluedict['end']
        giturl = keyvaluedict['giturl']
        to_addr = keyvaluedict['to_addr']
        
        subject = '%s @  %s' % (software, ip)
        
        
        #----------------------------------------------------------------------------------------------------------------------
        content = '开始从github获取源码：giturl（%s）' % giturl
        ggstools.mailAlert(subject, content,to_addr)
        result = step1conggithubhuoquyuanmaku.main(software, workhome, giturl)
        if result == True:
                content = '从github获取源码成功，giturl（%s）' % giturl
                ggstools.mailAlert(subject, content,to_addr)
        else:
                content = '从github获取源码失败，giturl（%s）' % giturl
                ggstools.mailAlert(subject, content,to_addr)
                raise Exception('error')
        print 'ok1'
          
        #----------------------------------------------------------------------------------------------------------------------
        content = '开始将提交列表导入数据库' 
        ggstools.mailAlert(subject, content,to_addr)
        result = step2gitloghuoqurizhixinxi.main(software, workhome)
        if result[0] == True:
                content = '提交列表导入数据库，共 %s 次提交' % result[1]
                ggstools.mailAlert(subject, content,to_addr)
        else:
                content = '提交列表获取失败' 
                ggstools.mailAlert(subject, content,to_addr)
                raise Exception('error')
        print 'ok2'
          
  
        #----------------------------------------------------------------------------------------------------------------------
        step3xuanqushiyuanbanben.main(software, start, end)
        content = '选取实验版本范围，从第 %s 次提交到第 %s 次提交' % (start, end)
        ggstools.mailAlert(subject, content,to_addr)
        print 'ok3'
         
         
        #----------------------------------------------------------------------------------------------------------------------
        #克隆检测
        content = '开始克隆检测' 
        ggstools.mailAlert(subject, content,to_addr)
        granularity = 'blocks'
        threshold = '0.30'
        rename='-blind' #-blind
        gitcodepath = os.path.join(workhome,  'gitcode')
        tmppath = os.path.join(workhome, 'tmp')
        step4kelongjiance.main(software, ip, language, granularity, threshold, rename, gitcodepath, tmppath, nicadpath,to_addr)
        print 'ok4'
        
        #----------------------------------------------------------------------------------------------------------------------
        #字段更新
        content = '开始字段更新' 
        ggstools.mailAlert(subject, content,to_addr)
        step5gengxinziduan.main(software, ip,to_addr)
        print 'ok5'
         
        #----------------------------------------------------------------------------------------------------------------------
        #克隆映射
        content = '开始相邻版本克隆映射' 
        ggstools.mailAlert(subject, content,to_addr)
        step6kelongyingse.main(software, ip,to_addr)
        print 'ok6'
        
        
        #----------------------------------------------------------------------------------------------------------------------
        #添加短期演化模式
        content = '根据相邻版本克隆映射，开始添加短期演化模式' 
        ggstools.mailAlert(subject, content,to_addr)
        step7tianjiayanhumoshi.main(software, ip,to_addr)
        print 'ok7'
        
        #----------------------------------------------------------------------------------------------------------------------
        content = '以克隆群为点、映射关系为边的图中，开始提取克隆谱系并识别长期演化模式' 
        ggstools.mailAlert(subject, content,to_addr)
        #提取克隆谱系并识别长期演化模式
        step8tiqukelongpuxibingshibieyanhuamoshi.main(software, ip, to_addr)
        print 'ok8'
        
        content = '多版本克隆演化痕迹构建成功，相关信息请查询数据库' 
        ggstools.mailAlert(subject, content,to_addr)
        print 'ok'
        #可以直接运行8了,下次别忘了改起始克隆谱系编号
# #         #统计结果
# #         step9shujutongji.main(software, ip, workhome)
#         