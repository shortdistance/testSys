# -*- coding: utf-8 -*-
# 是否调试模式
DEBUG = True

# 主机IP
# HOST = '127.0.0.1'
HOST = '0.0.0.0'

# 主机端口
PORT = 11001

# Cookie安全密钥
SECRET_KEY = 'TestSysSecret'

# Session超时时间
SESSION_TIMEOUT = 60 * 60

# 分页单页条数
PAGESIZE = 20

# 上传文件目录
import os

UPLOADDIR = 'Uploads'
UPLOADPATH = os.path.join(os.path.dirname(__file__), UPLOADDIR)
CASE_ATTACHMENT_SUBPATH = 'Case/Attachment'
CASE_AUTORUN_SUBPATH = 'Case/AutoCase'
CASE_IMPORT_SUBPATH = 'Case/CaseImport'
TASK_ATTACHMENT_SUBPATH = 'Task/Attachment'
ISSUE_ATTACHMENT_SUBPATH = 'Issue/Attachment'
ISSUE_IMPORT_SUBPATH = 'Issue/IssueImport'

CASE_ATTACHMENT_UPLOAD_PATH = UPLOADPATH + '/' + CASE_ATTACHMENT_SUBPATH
CASE_AUTORUN_UPLOAD_PATH = UPLOADPATH + '/' + CASE_AUTORUN_SUBPATH
TASK_ATTACHMENT_UPLOAD_PATH = UPLOADPATH + '/' + TASK_ATTACHMENT_SUBPATH
ISSUE_ATTACHMENT_UPLOAD_PATH = UPLOADPATH + '/' + ISSUE_ATTACHMENT_SUBPATH
ISSUE_IMPORT_UPLOAD_PATH = UPLOADPATH + '/' + ISSUE_IMPORT_SUBPATH

# 第三方工具或者jar包目录
UTILSDir = 'Utils'
UTILSPATH = os.path.join(os.path.dirname(__file__), UTILSDir)

# 开启邮件通知
ENABLE_MAIL_NOTICE = False
# 邮件服务器
SMTP_HOST = 'smtp.163.com'
# 发件人
SMTP_USER = 'zhanglei520vip@163.com'
# 密码
SMTP_PASS = '1qaz2wsx'

# 数据库连接串
# DB = 'sqlite:///TestSys.sqlite'
# mysql
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/testsys1?charset=utf8'
DBLinkStr = 'root:123456@127.0.0.1:3306/testsys1'
SQLALCHEMY_POOL_SIZE = 80

# 页面加载停顿时间
PAGE_LOAD_WAIT = 0.1

# WIN, LINUX
HOST_OS = 'WIN'
# WIN: 200ms, LINUX:1s
PING_TIMEOUT = {'WIN': 200, 'LINUX': 1}
