#-*- coding:utf-8 -*-
import jpype
import os

    
def SendMail(smtpserver,smtpport, mailuser, mailpwd, jmailJar, msgto, msgfrom, subject,  body):
    '''
    msgto = 'zhangleid@si-tech.com.cn'
    msgfrom = 'zhangleid@si-tech.com.cn' 
    
    subject = u'subject'
    body = u"""
    Hi:
        how are you 
        
    """
    smtpserver = 'smtp.si-tech.com.cn'     #smtp server
    smtpport = 25
    mailuser = 'zhangleid@si-tech.com.cn'  #username
    mailpwd = '1qaz2wsx'                   #passwd
    jmailJar = '.\\jmail.jar'
    sendattachmail(smtpserver,smtpport, mailuser, mailpwd, jmailJar, msgto, msgfrom, subject,  body1)
    '''
    
    jpype.startJVM("%s/jre/bin/client/jvm.dll"%(os.environ.get("JAVA_HOME")), "-ea","-Djava.class.path=%s" % jmailJar)
    JDClass = jpype.JClass("com.ykmaiz.mail.MailSupport")
    try:
        jd = jpype.JPackage("com.ykmaiz.mail").MailSupport(smtpserver, mailuser, mailpwd, False)
        jd.send(msgfrom, msgto, subject, body); 

    except Exception, e:
        print e
    jpype.shutdownJVM()  


if __name__ == '__main__':
    msgto = 'zhangleid@si-tech.com.cn'
    msgfrom = 'zhangleid@si-tech.com.cn' 
    
    subject = u'主题'
    body = 'hello world'
    body1=u"""
    Hi:
        你好
        
    """

    smtpserver = 'smtp.si-tech.com.cn'     #smtp server
    smtpport = 25
    mailuser = 'zhangleid@si-tech.com.cn'  #用户名
    mailpwd = '1qaz2wsx'                   #密码
    jmailJar = '.\\jmail.jar'
    SendMail(smtpserver,smtpport, mailuser, mailpwd, jmailJar, msgto, msgfrom, subject,  body1)



