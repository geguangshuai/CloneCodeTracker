#coding=utf-8
from dao import *
import Levenshtein

'''
计算两个字符串的编辑距离相似度
'''
def calculateLevenshtein(s1, s2):
        fz = Levenshtein.distance(s1,s2)
        fm = len(s1)
        if len(s2) > fm:
                fm = len(s2)
        return 1.0 - 1.0*fz/fm

'''
对一个克隆片段内容token化
'''      
def makeToken(oldstr):
        symbols = ',.;:?\'"([{%^-<>!|/\\~#)]}&*=+'
        keywordDict =  {'auto' : 'A', 'struct' : 'S', 'break' : 'B', 'else' : 'E', 'switch' : 'S', 'case' : 'C', 'enum' : 'E', 'register' : 'R', 'typedef' : 'T', 'extern' : 'E', 'return' : 'R', 'union' : 'U', 'const' : 'C', 'continue' : 'C', 'for' : 'F', 'default' : 'D', 'goto' : 'G', 'sizeof' : 'S', 'volatile' : 'V', 'do' : 'D', 'while' : 'W', 'static' : 'S' }
        #第一步，对老的字符串，符号的左右加空格，形成新的字符串
        newlist = []
        for char in oldstr:
                if char in symbols:
                        newlist.append(' ' + char + ' ')
                else:
                        newlist.append(char)
        newstr = ''.join(newlist)
        #第二步，以空格分割，形成每一个单词，按规则替换
        wordlist = newstr.split()
        tokenlist = []
        strcontent = False
        for word in wordlist:
                if strcontent == True:#如果在字符串内容阶段
                        if word == '"':#如果是“，说明字符串结束了，添加S，并终止字符串阶段
                                tokenlist.append('S')
                                strcontent = False
                else:#非字符串内容阶段
                        if word == '"':
                                strcontent = True
                        else:
                                keywordvalue = keywordDict.get(word, None)
                                if keywordvalue != None:#如果是关键字（除去int、float、double等数据类型）
                                        tokenlist.append(keywordvalue)
                                        continue
                                if word[0] in '0123456789' and word[-1] in '0123456789':#如果是数字，用D替换
                                        tokenlist.append('D')
                                        continue
                                if word in symbols:#如果是符号，保留
                                        tokenlist.append(word)
                                        continue
                                tokenlist.append('V')#一般变量，用V
                        #end else 非字符串内容阶段
        #end for
        tokenstr = ''.join(tokenlist)
        return tokenstr

def clonefragmentSimilarityInCloneClass(cloneclass):
        clonefragmentDao = CloneFragmentDao()
        pcidlist = cloneclass.pcidset.split('-')
        tokenlist = []
        for pcid in pcidlist:
                source = clonefragmentDao.getSource(cloneclass.version, pcid)
                token = makeToken(source)
                #print token
                tokenlist.append(token)
        
        similaritylist = []
        for i in range(len(tokenlist)-1):
                for j in range(i+1, len(tokenlist)):
                        similarity = calculateLevenshtein(tokenlist[i], tokenlist[j])
                        similaritylist.append(similarity)
#         print '-'*10
#         print cloneclass.classid
#         print similaritylist
        return similaritylist

def clonefragmentSimilarityInCloneClassOfVersion(version):
        cloneclassDao = CloneClassDao()
        cloneclasslist = cloneclassDao.selectAllCloneClassForVersion(version)
        resultlist = [0 for i in range(11)]
        for cloneclass in cloneclasslist:
                similaritylist = clonefragmentSimilarityInCloneClass(cloneclass)
                similarity = min(similaritylist)
                if similarity>=1.0:
                        resultlist[10] = resultlist[10]  + 1
                elif similarity>=0.9:
                        resultlist[9] = resultlist[9]  + 1
                elif similarity>=0.8:
                        resultlist[8] = resultlist[8]  + 1
                elif similarity>=0.7:
                        resultlist[7] = resultlist[7]  + 1
                elif similarity>=0.6:
                        resultlist[6] = resultlist[6]  + 1
                elif similarity>=0.5:
                        resultlist[5] = resultlist[5]  + 1
                elif similarity>=0.4:
                        resultlist[4] = resultlist[4]  + 1
                elif similarity>=0.3:
                        resultlist[3] = resultlist[3]  + 1
                elif similarity>=0.2:
                        resultlist[2] = resultlist[2]  + 1
                elif similarity>=0.1:
                        resultlist[1] = resultlist[1]  + 1
                elif similarity>=0.0:
                        resultlist[0] = resultlist[0]  + 1
        print resultlist

if __name__ == '__main__':
        version = 'ant1342'
        clonefragmentSimilarityInCloneClassOfVersion(version)
        