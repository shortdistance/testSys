# -*- coding: utf-8 -*-
from flask import render_template, request, jsonify, g
from scripts.services import userprofile
from . import bp_main as main
# 加日志
from scripts.services.log import addLog, ActionType


@main.route('/Admin')
def admin_index():
    return render_template('Admin/index.html')


@main.route('/QueryUser', methods=['POST'])
def query_user():
    mail_or_nick = request.json['Word']
    status = request.json['Status']
    page_no = request.json['PageNo']

    (row_count, page_count, page_no, page_size, data) = userprofile.query_user(mail_or_nick, int(status),
                                                                               "RegDate desc", page_no)
    user_list = []
    for i in data.all():
        user_list.append(
            {'UserId': i.UserId, 'Email': i.Email, 'Nick': i.Nick, 'Status': i.Status, 'IsAdmin': i.IsAdmin,
             'RegDate': i.RegDate.isoformat()})
    return jsonify(row_count=row_count, page_count=page_count, page_no=page_no, page_size=page_size, data=user_list)


@main.route('/EnableUser', methods=['POST'])
def enable_user():
    userid = request.json['UserId']
    userprofile.enable_user(userid)

    # ---------加日志-----------
    username = userprofile.get_user_by_id(userid).Nick
    addLog(0, g.nick, ActionType.admin_enable_user, username)
    # --------------------------
    return jsonify(status='ok')


@main.route('/DisableUser', methods=['POST'])
def disable_user():
    userid = request.json['UserId']
    userprofile.disable_user(userid)
    # ---------加日志-----------
    username = userprofile.get_user_by_id(userid).Nick
    addLog(0, g.nick, ActionType.admin_disable_user, username)
    # --------------------------
    return jsonify(status='ok')


@main.route('/ResetPassword', methods=['POST'])
def reset_password():
    userid = request.json['UserId']
    userprofile.reset_password(userid)
    # ---------加日志-----------
    username = userprofile.get_user_by_id(userid).Nick
    addLog(0, g.nick, ActionType.admin_reset_password, username)
    # --------------------------
    return jsonify(status='ok')


@main.route('/AssignAdmin', methods=['POST'])
def assign_admin():
    userid = request.json['UserId']
    userprofile.assign_admin(userid)
    # ---------加日志-----------
    username = userprofile.get_user_by_id(userid).Nick
    addLog(0, g.nick, ActionType.admin_assign_admin, username)
    # --------------------------
    return jsonify(status='ok')
