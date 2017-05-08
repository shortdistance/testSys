# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, session, jsonify, g
from scripts.services import userprofile
from . import bp_main as main
# 加日志
from scripts.services.log import addLog, ActionType


@main.route('/SignOut')
def user_sign_out():
    # ---------加日志-----------
    addLog(0, g.nick, ActionType.user_sign_out)
    # --------------------------
    session['username'] = None
    session['userid'] = None
    session['nick'] = None
    return redirect('/')


@main.route('/Profile')
def user_profile():
    u = userprofile.get(session['username'])
    return render_template('Profile/Detail.html', User=u)


@main.route('/ChangePassword', methods=['POST'])
def user_change_password():
    raw_password = request.json['RawPassword']
    password = request.json['Password']
    updated = userprofile.change_password(raw_password, password, g.user_id)
    # ---------加日志-----------
    addLog(0, g.nick, ActionType.user_change_password)
    # --------------------------
    return jsonify(Updated=updated)


@main.route('/UpdateProfile', methods=['POST'])
def user_update_profile():
    email = request.json['Email']
    nick = request.json['Nick']
    updated = userprofile.udpate_profile(email, nick, g.user_id)
    if updated:
        session['username'] = email
        # ---------加日志-----------
        addLog(0, g.nick, ActionType.user_update_profile)
        # --------------------------
    return jsonify(Updated=updated)
