# -*- coding: utf-8 -*-
from flask import render_template, jsonify, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import *
from scripts.services import userprofile
from scripts.models.userprofile import UserStatus
from scripts.config import *
from . import bp_login
import time
# 日志
from scripts.services.log import addLog, ActionType


@bp_login.route('/')
def index():
    if 'username' in session and not session['username'] == None:
        time.sleep(PAGE_LOAD_WAIT)
        return redirect('/MyZone')
    return render_template('Login.html')


@bp_login.route('/Login', methods=['POST'])
def login():
    email = request.json['Email']
    password = request.json['Password']
    user = userprofile.get(email)
    if user == None:
        response = jsonify(isDisabled=False, isMatch=False)
        return response

    if user.Status == UserStatus.Disabled:
        response = jsonify(isDisabled=True, isMatch=None)
        return response

    # if not user.Password == password:
    if not check_password_hash(user.Password, password):
        response = jsonify(isDisabled=False, isMatch=False)
        return response

    session.permanent = False
    session['userid'] = user.UserId
    session['nick'] = user.Nick
    session['username'] = user.Email
    session['isadmin'] = user.IsAdmin

    response = jsonify(isDisabled=False, isMatch=True)
    # ---------加日志-----------
    addLog(0, user.Nick, ActionType.home_login)
    # --------------------------
    return response


@bp_login.route('/Register')
def register():
    time.sleep(PAGE_LOAD_WAIT)
    return render_template('Register.html')


'''
request: {"Nick":"23","Password":"123","ConfirmPassword":"123","Email":"3@3.com"}
response: {"created": true}
'''


@bp_login.route('/Register/Save', methods=['POST'])
def register_save():
    email = request.json['Email']
    nick_name = request.json['Nick']
    password = generate_password_hash(request.json['Password'])
    (exist, userid) = userprofile.register(email, nick_name, password)
    if not exist:
        session['userid'] = userid
        session['username'] = request.json['Email']
        session['nick'] = request.json['Nick']
        # ---------加日志-----------
        addLog(0, session['nick'], ActionType.home_register_save)
    # --------------------------

    session['isadmin'] = False
    result = {'created': not exist}
    return jsonify(result)


# For web install 安装完毕后，请从此处开始删除*************************************************
@bp_login.route('/Install')
def db_install():
    import sys
    from scripts.models import database
    from scripts.models.userprofile import UserProfile, UserStatus
    from scripts.models.project import Project, ProjectStatus
    from scripts.models.member import Member
    from scripts.models.issue import \
        IssueStatus, IssueCategoryStatus, \
        IssuePriority, IssueCategory, \
        IssueHistory, Issue
    from scripts.models.task import TaskPriority, TaskStatus, Task
    from scripts.models.comment import CommentType, Comment
    from scripts.models.file import ObjectType, FileUpload
    from scripts.models.case import TestCaseType, TestCaseResultType, \
        TestCase, TestCaseHistory, \
        TestCaseMapFieldAndValue, TestCaseLinkBug, \
        TestCaseResult, AutoRunScript, \
        ScriptPostDataField, OperType, \
        ScriptParameterBind, AutoRunHistory
    from scripts.models.customfield import ObjectType, CustomField, CustomFieldValue
    from scripts.models.log import ActionType, JsonActionTypeDetailList, ActionLog
    from scripts.models.monitor import HostMonitor

    from datetime import datetime

    database.drop_database()
    print(u'删除数据库完成')
    database.create_database()
    print(u'创建数据库完成')

    session = database.get_session()
    admin = UserProfile()
    admin.Email = 'admin@admin.com'
    admin.Nick = u'admin'
    admin.Password = 'admin'
    admin.Status = UserStatus.Enabled
    admin.IsAdmin = True
    admin.RegDate = datetime.now()
    session.add(admin)

    bug = IssueCategory()
    bug.CategoryName = u'Bug'
    bug.Status = IssueCategoryStatus.Enabled
    session.add(bug)

    issue = IssueCategory()
    issue.CategoryName = u'Issue'
    issue.Status = IssueCategoryStatus.Enabled
    session.add(issue)

    session.commit()
    session.close()
    return u'TestSys安装完成'

    # For web install 安装完毕后，删除结束*******************************************************
