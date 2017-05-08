# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from scripts.config import *

# 兼容2.x和3.x
try:
    import _thread
except:
    import thread


def send_mail(mail_to, subject, body):
    def _send(mail_to, subject, body):
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = SMTP_USER
        msg['To'] = mail_to
        content = MIMEText(body, 'html', 'utf-8')
        msg.attach(content)
        try:
            smtp = smtplib.SMTP_SSL()
            smtp.connect(SMTP_HOST)
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.sendmail(SMTP_USER, msg['To'].split(','), msg.as_string())
        except Exception, e:
            print e.message

    if ENABLE_MAIL_NOTICE:
        thread.start_new_thread(_send, (mail_to, subject, body))


def render_mail_template(template_path, **kwargs):
    env = Environment(loader=FileSystemLoader('scripts/templates/Mail/'))
    template = env.get_template(template_path)
    return template.render(**kwargs)
