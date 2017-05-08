# -*- coding: utf-8 -*-
from flask import render_template, request, jsonify, g
from scripts.services import team, project
from . import bp_main as main
# 加日志
from scripts.services.log import addLog, ActionType


@main.route('/Project/Team/<int:project_id>')
def team_list(project_id):
    p = project.get(project_id)
    return render_template('Team/List.html', ProjectId=project_id, Creator=p.Creator, CurrentUser=g.user_id)


@main.route('/Team/GetMemberCandidate', methods=['POST'])
def team_member_candidate():
    project_id = request.json['ProjectId']
    member_list = team.member_candidate(project_id)
    result = []
    for m in member_list:
        result.append({'Email': m.Email, 'Nick': m.Nick})
    return jsonify(data=result)


@main.route('/Team/GetMemberInProject', methods=['POST'])
def team_member_in_project():
    project_id = request.json['ProjectId']
    member_list = team.member_in_project(project_id)
    result = []
    for m in member_list:
        result.append({'Email': m.Email, 'Nick': m.Nick, 'UserId': m.UserId})
    return jsonify(data=result)


@main.route('/Team/AddMember', methods=['POST'])
def team_add_member():
    project_id = request.json['ProjectId']
    email = request.json['Email']
    team.add_member(project_id, email)
    # ---------加日志-----------
    addLog(project_id, g.nick, ActionType.team_add_member, email)
    # --------------------------
    return jsonify(created=True)


@main.route('/Team/RemoveMember', methods=['POST'])
def team_remove_member():
    project_id = request.json['ProjectId']
    user_id = request.json['UserId']
    team.remove_member(project_id, user_id)
    # ---------加日志-----------
    addLog(project_id, g.nick, ActionType.team_remove_member, 'UserId: %d' % user_id)
    # --------------------------
    return jsonify(removed=True)
