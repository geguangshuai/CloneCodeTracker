#coding=utf-8
import os
import shutil
from ggstools import *

def getCodeRepositoryFromGitHub(software, giturl, gitcodedirpath):
        #如果gitcode目录不存在，创建一个目录
        if not os.path.isdir(gitcodedirpath):
                os.mkdir(gitcodedirpath)
        softwarepath = os.path.join(gitcodedirpath, software)
        if os.path.isdir(softwarepath):
                shutil.rmtree(softwarepath)
                
        #进入gitcode目录，使用git clone命令将软件源码从github上拷贝下来
        os.chdir(gitcodedirpath)
        git_clone_cmd = 'git clone %s' % giturl
        result = os.system(git_clone_cmd)
        if result==0:
                return True
        else:
                return False


def main(software,  workhome,  giturl):
        gitcodedirpath = os.path.join(workhome, 'gitcode')
        result = getCodeRepositoryFromGitHub(software, giturl, gitcodedirpath)
        return result
        
        
        
        