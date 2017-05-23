#coding=utf-8
from ggstools import *

if __name__ == '__main__':
        subject = 'test'
        content = 'test'
        mailAlert(subject, content)
        
        keyvaluedict = readConfig()
        for key in keyvaluedict.keys():
                print key
                print keyvaluedict[key]