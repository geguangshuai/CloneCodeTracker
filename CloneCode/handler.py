#coding=utf-8
import xml.sax
from bean import *

'''
<source file="/home/ggs/workspacMultipartConfigElement.java" startline="32" endline="42">
......
</source>
'''
class CloneFragmentHandler(xml.sax.ContentHandler):
        def __init__(self, version):#version,pcid, file, startline, endline, source
                self.version, self.clonefragmentlist, self.pcid, self.file, self.startline, self.endline, self.source = version, [], 0, None, None, None, None
                self.newstart = False
        
        def startElement(self, name, attrs):
                if name == 'source':
                        self.file, self.startline, self.endline, self.pcid, self.source = attrs['file'], attrs['startline'], attrs['endline'], self.pcid + 1, []
                        self.newstart = True
        
        def endElement(self, name):
                if name == 'source':#version, pcid, file, startline, endline, source
                        self.clonefragmentlist.append(CloneFragment(self.version, self.pcid, self.file, self.startline, self.endline, ''.join(self.source)))
                        self.file, self.startline, self.endline, self.source = None, None, None, None
                        self.newstart = False
        
        def characters(self, content):
                if self.newstart == True:
                        self.source.append(content)


'''
<class classid="1" nclones="3" nlines="336" similarity="73">
<source file="coyote/http11/Http11Processor.java" startline="638" endline="957" pcid="24747"></source>
</class>
'''
class CloneClassHandler(xml.sax.ContentHandler):
        def __init__(self, version):#version, classid, nclones, nlines, similarity, pcidset
                self.cloneclasslist, self.version, self.classid, self.nclones, self.nlines, self.similarity, self.pcidset = [], version, None, None, None, None, None
    
        def startElement(self, name, attrs):
                if name == 'class':
                        self.classid, self.nclones, self.nlines, self.similarity, self.pcidset  =  attrs['classid'], attrs['nclones'], attrs['nlines'], attrs['similarity'], [], 
                if name == 'source':
                        self.pcidset.append(attrs['pcid'])
            
        def endElement(self, name):
                if name == 'class':#version, classid, nclones, nlines, similarity, pcidset
                        self.cloneclasslist.append(CloneClass(self.version, self.classid, self.nclones, self.nlines, self.similarity, '-'.join(self.pcidset)))
                        self.classid, self.nclones, self.nlines, self.similarity, self.pcidset = None, None, None, None, None
            
        def characters(self, content):
                pass

