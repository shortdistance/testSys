# -*- coding: utf-8 -*-
from scripts.models.database import BaseModel
from scripts.models.project import Project, ProjectStatus
from scripts.models.userprofile import UserStatus, UserProfile
from sqlalchemy import Column, Integer, SMALLINT, String, Boolean, DateTime, Float, ForeignKey, UnicodeText
from sqlalchemy.orm import relationship


class ActionType:
    home_login = 101
    home_register_save = 102
    user_sign_out = 121
    user_change_password = 122
    user_update_profile = 123
    project_create = 201
    project_delete = 202
    project_update = 203
    admin_enable_user = 301
    admin_disable_user = 302
    admin_reset_password = 303
    admin_assign_admin = 304
    setting_enable_customfield = 401
    setting_disable_customfield = 402
    setting_delete_customfield = 403
    setting_saveFieldDesc = 404
    setting_create_customfield = 405
    setting_enable_fieldvalue = 406
    setting_disable_fieldvalue = 407
    setting_delete_fieldvalue = 408
    setting_save_fieldvalue = 409
    setting_create_fieldvalue = 410
    task_create = 501
    task_update = 502
    task_delete = 503
    case_create = 601
    case_update = 602
    case_delete = 603
    case_execute = 604

    issue_create = 701
    issue_update = 702
    issue_delete = 703
    comment_createComment = 801
    team_add_member = 901
    team_remove_member = 902


JsonActionTypeDetailList = [
    {'op_code': 101, 'op_string': 'home_login', 'op_detail': u'[%s]登陆'},
    {'op_code': 102, 'op_string': 'home_register_save', 'op_detail': u'[%s]注册'},
    {'op_code': 121, 'op_string': 'user_sign_out', 'op_detail': u'[%s]退出'},
    {'op_code': 122, 'op_string': 'user_change_password', 'op_detail': u'[%s]修改密码'},
    {'op_code': 123, 'op_string': 'user_update_profile', 'op_detail': u'[%s]修改用户信息'},
    {'op_code': 201, 'op_string': 'project_create', 'op_detail': u'[%s]创建项目[%s]'},
    {'op_code': 202, 'op_string': 'project_delete', 'op_detail': u'[%s]删除项目[%s]'},
    {'op_code': 203, 'op_string': 'project_update', 'op_detail': u'[%s]更改项目[%s]信息'},
    {'op_code': 301, 'op_string': 'admin_enable_user', 'op_detail': u'[%s]启用用户[%s]'},
    {'op_code': 302, 'op_string': 'admin_disable_user', 'op_detail': u'[%s]禁用用户[%s]'},
    {'op_code': 303, 'op_string': 'admin_reset_password', 'op_detail': u'[%s]重置[%s]的密码'},
    {'op_code': 304, 'op_string': 'admin_assign_admin', 'op_detail': u'[%s]给[%s]分配管理员权限'},
    {'op_code': 401, 'op_string': 'setting_enable_customfield', 'op_detail': u'[%s]启用自定义字段[%s]'},
    {'op_code': 402, 'op_string': 'setting_disable_customfield', 'op_detail': u'[%s]禁用自定义字段[%s]'},
    {'op_code': 403, 'op_string': 'setting_delete_customfield', 'op_detail': u'[%s]删除自定义字段[%s]'},
    {'op_code': 404, 'op_string': 'setting_saveFieldDesc', 'op_detail': u'[%s]保存自定义字段[%s]描述'},
    {'op_code': 405, 'op_string': 'setting_create_customfield', 'op_detail': u'[%s]创建自定义字段[%s]'},
    {'op_code': 406, 'op_string': 'setting_enable_fieldvalue', 'op_detail': u'[%s]启用字段值[%s]'},
    {'op_code': 407, 'op_string': 'setting_disable_fieldvalue', 'op_detail': u'[%s]禁用字段值[%s]'},
    {'op_code': 408, 'op_string': 'setting_delete_customfield', 'op_detail': u'[%s]删除字段值[%s]'},
    {'op_code': 409, 'op_string': 'setting_save_fieldvalue', 'op_detail': u'[%s]保存字段值[%s]'},
    {'op_code': 410, 'op_string': 'setting_create_fieldvalue', 'op_detail': u'[%s]创建字段值[%s]'},
    {'op_code': 501, 'op_string': 'task_create', 'op_detail': u'[%s]创建任务[%s]'},
    {'op_code': 502, 'op_string': 'task_update', 'op_detail': u'[%s]更新任务[%s]'},
    {'op_code': 503, 'op_string': 'task_delete', 'op_detail': u'[%s]删除任务[%s]'},
    {'op_code': 601, 'op_string': 'case_create', 'op_detail': u'[%s]创建测试用例[%s]'},
    {'op_code': 602, 'op_string': 'case_update', 'op_detail': u'[%s]更新测试用例[%s]'},
    {'op_code': 603, 'op_string': 'case_delete', 'op_detail': u'[%s]删除测试用例[%s]'},
    {'op_code': 604, 'op_string': 'case_execute', 'op_detail': u'[%s]执行测试用例[%s]'},

    {'op_code': 701, 'op_string': 'issue_create', 'op_detail': u'[%s]创建问题[%s]'},
    {'op_code': 702, 'op_string': 'issue_update', 'op_detail': u'[%s]更新问题[%s]'},
    {'op_code': 703, 'op_string': 'issue_delete', 'op_detail': u'[%s]删除问题[%s]'},
    {'op_code': 801, 'op_string': 'comment_createComment', 'op_detail': u'[%s]发表评论[%s]'},
    {'op_code': 901, 'op_string': 'team_add_member', 'op_detail': u'[%s]增加团队成员[%s]'},
    {'op_code': 902, 'op_string': 'team_remove_member', 'op_detail': u'[%s]删除团队成员[%s]'}
]


class ActionLog(BaseModel):
    __tablename__ = 'ActionLog'
    LogId = Column('LogId', Integer, primary_key=True, autoincrement=True)
    ProjectId = Column('ProjectId', Integer)
    ProjectProfile = relationship('Project', foreign_keys=ProjectId, primaryjoin=ProjectId == Project.ProjectId)
    UserName = Column('UserName', String(16))
    ActionType = Column('ActionType', Integer)
    CreateTime = Column('CreateTime', DateTime)
    ActionDetail = Column('ActionDetail', String(255), nullable=True)
