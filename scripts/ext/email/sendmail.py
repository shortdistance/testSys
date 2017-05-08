#!/bin/env python
#-*-coding:utf-8-*-

import string
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')
import ConfigParser
import smtplib
from email.mime.text import MIMEText
from email.message import Message
from email.header import Header


def send_mail(mail_host,mail_port,mail_user,mail_pass,send_mail_from, to_list,sub,content):
    me=send_mail_from
    msg = MIMEText(content, _subtype='html', _charset='utf8')
    msg['Subject'] = Header(sub,'utf8')
    msg['From'] = Header(me,'utf8')
    msg['To'] = ";".join(to_list)
    try:

        smtp = smtplib.SMTP()
        #smtp.set_debuglevel(1)
        smtp.connect(mail_host,mail_port)
        smtp.login(mail_user, mail_pass)
        smtp.sendmail(me, to_list, msg.as_string())
        smtp.close()
        return True
    except Exception, e:
        print str(e)
        return False


if __name__ == '__main__':
    SMTP_HOST = 'smtp.si-tech.com.cn'
    SMTP_PORT = 25
    SMTP_USER = 'tmsupport@si-tech.com.cn'
    SMTP_PASS = '295220'
    
    mail_to = ['zhangleid@si-tech.com.cn']
    subject = 'hello world'
    body = '123'
    send_mail(SMTP_HOST,SMTP_PORT,SMTP_USER,SMTP_PASS,SMTP_USER, mail_to,subject,body)
