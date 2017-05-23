#coding=utf-8

import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import ConfigParser

def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr(( Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def mailAlert(subject, content,to_addr):
#         print subject
#         print content
#         return 
        
        smtp_server = 'smtp.sina.com' #smtp.163.com # smtp.sina.com
        server = smtplib.SMTP(smtp_server, 25)
        from_addr = 'geguangshuai@sina.cn' #  Passw0rd
        password = 'Passw0rd'
        server.login(from_addr, password)
        #构造邮件内容
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['Subject'] = Header('CloneCodeTracker运行通知：' + subject, 'utf-8').encode()
        msg['From'] = _format_addr('CloneCodeTracker提醒邮箱 <%s>' % from_addr)
        msg['To'] = _format_addr(to_addr)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()

#读取配置文件
def readConfig():
        cp = ConfigParser.SafeConfigParser()
        cp.read('ggs.config')
        keyvaluelist = cp.items('codeclone')
        keyvaluedict = {}
        for (key,value) in keyvaluelist:
                keyvaluedict[key] = value
                
        if len(keyvaluedict['giturl']) > 0:
                if keyvaluedict['giturl'][0] == '"':
                        keyvaluedict['giturl'] = keyvaluedict['giturl'][1:]
                if keyvaluedict['giturl'][-1] == '"':
                        keyvaluedict['giturl'] = keyvaluedict['giturl'][:-1]
        
        if len(keyvaluedict['start']) > 0:
                keyvaluedict['start'] = int(keyvaluedict['start'])
        if len(keyvaluedict['end']) > 0:
                keyvaluedict['end'] = int(keyvaluedict['end']) 
                
        return keyvaluedict