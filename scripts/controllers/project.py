# -*- coding: utf-8 -*-
from flask import render_template, jsonify, request, g
from scripts.models.util import SequenceType
from scripts.services import project, task, issue, team, log, util
from . import bp_main as main
# 加日志
from scripts.services.log import addLog, ActionType


@main.route('/MyZone')
def proj_index():
    return render_template('Project/List.html')


@main.route('/Project/Query', methods=['POST'])
def proj_query():
    project_name = request.json['ProjectName']
    status = int(request.json['Status'])
    page_no = int(request.json['PageNo'])

    (row_count, page_count, page_no, page_size, data) = project.query(project_name, status, page_no,
                                                                      'CreateDate desc', g.user_id)
    projects = []
    for p in data.all():
        projects.append(
            {'ProjectId': p.ProjectId, 'ProjectName': p.ProjectName, 'Status': p.Status, 'Progress': p.Progress,
             'CreateDate': p.CreateDate.isoformat(), 'Creator': p.UserProfile.Nick})

    return jsonify(row_count=row_count, page_count=page_count, page_no=page_no, page_size=page_size, data=projects)


@main.route('/Project/Create', methods=['GET'])
def proj_create():
    return render_template('Project/Create.html')


@main.route('/Project/NewCreate', methods=['POST'])
def proj_newcreate():
    projectname = u'%s' % request.json['ProjectName']
    projectprefix = u'%s' % request.json['ProjectPrefix']

    if projectname and projectprefix:
        projectid = project.create(projectname, projectprefix, g.user_id)
        if projectid:
            # ---------加日志-----------
            addLog(0, g.nick, ActionType.project_create,
                   '<a href="/Project/Dashboard/%d">%s</a>' % (projectid, projectname))
            # --------------------------

            # 给该项目创建三个自增序列(case, task, issue)
            util.create_sequence('C%s' % (projectprefix), SequenceType.Case, projectid)
            util.create_sequence('T%s' % (projectprefix), SequenceType.Task, projectid)
            util.create_sequence('I%s' % (projectprefix), SequenceType.Issue, projectid)
    return jsonify(created=True)


@main.route('/Project/Delete', methods=['POST'])
def proj_delete():
    try:
        projectid = request.json['ProjectId']
        projectname = project.get(projectid).ProjectName
        project.delete(projectid)
    except Exception, e:
        print e.message
        return jsonify(deleted=False)

    # ---------加日志-----------
    addLog(projectid, g.nick, ActionType.project_delete, projectname)
    # --------------------------
    return jsonify(deleted=True)


@main.route('/Project/Detail/<int:project_id>')
def proj_detail(project_id):
    proj = project.get(project_id)
    return render_template('Project/Detail.html', Project=proj, CreatorName=proj.UserProfile.Nick,
                           CurrentUser=g.user_id)


@main.route('/Project/Update', methods=['POST'])
def proj_update():
    project_id = int(request.json['ProjectId'])
    project_name = request.json['ProjectName']
    project_prefix = request.json['ProjectPrefix']
    status = int(request.json['Status'])
    project.update(project_id, project_name, project_prefix, status)
    # ---------加日志-----------
    addLog(project_id, g.nick, ActionType.project_update,
           '<a href="/Project/Dashboard/%d">%s</a>' % (project_id, project_name))
    # --------------------------
    return jsonify(updated=True)


@main.route('/Project/Dashboard/<int:project_id>')
def proj_dashboard(project_id):
    (task_status, task_priority) = task.statistics(project_id)
    (issue_status, issue_priority) = issue.statistics(project_id)
    proj = project.get(project_id)
    member_list = team.member_in_project(project_id)
    return render_template('Project/Dashboard.html', Project=proj, TaskStatus=task_status,
                           TaskPriority=task_priority, IssueStatus=issue_status, IssuePriority=issue_priority,
                           MemberList=member_list)


@main.route('/Project/Log', methods=['POST'])
def proj_get_log():
    page_no = int(request.json['PageNo'])
    (row_count, page_count, page_no, page_size, data) = log.getlog(page_no)

    loglist = []
    for i in data.all():
        loglist.append({'LogId': i.LogId, 'ProjectId': i.ProjectId, 'UserName': i.UserName, 'ActionType': i.ActionType,
                        'CreateTime': i.CreateTime.strftime("%Y-%m-%d %H:%M:%S"), 'ActionDetail': i.ActionDetail})
    return jsonify(row_count=row_count, page_count=page_count, page_no=page_no, page_size=page_size, data=loglist)
