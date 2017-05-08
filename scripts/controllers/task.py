# -*- coding: utf-8 -*-
from flask import render_template, request, jsonify, g
from scripts.services import task, team
from . import bp_main as main
# 加日志
from scripts.services.log import addLog, ActionType
from scripts.models.util import SequenceType
from scripts.services import util


@main.route('/Project/Task/<int:project_id>')
def task_list(project_id):
    member_list = team.member_in_project(project_id)
    return render_template('Task/List.html', ProjectId=project_id, MemberList=member_list)


@main.route('/Task/Query', methods=['POST'])
def task_query():
    projectid = int(request.json['ProjectId'])
    task_name = request.json['TaskName']
    task_type = int(request.json['TaskType'])
    assign_to = int(request.json['AssignTo'])
    if assign_to == -1:
        assign_to = g.user_id
    status_new = request.json['New']
    status_in_progress = request.json['InProgress']
    status_completed = request.json['Completed']
    status_canceled = request.json['Canceled']
    page_no = int(request.json['PageNo'])
    (row_count, page_count, page_no, page_size, data) = task.query(projectid, task_name, task_type, assign_to,
                                                                   status_new, status_in_progress,
                                                                   status_completed, status_canceled,
                                                                   'CreateDate Desc', page_no)
    tasks = []
    for t in data.all():
        tasks.append({'TaskId': t.TaskId,
                      'ProjectId': t.ProjectId,
                      'TaskName': t.TaskName,
                      'TaskType': t.TaskType,
                      'Priority': t.Priority,
                      'Progress': t.Progress,
                      'Status': t.Status,
                      'Effort': t.Effort,
                      'AssignTo': t.AssignToProfile.Nick,
                      'Creator': t.CreatorProfile.Nick,
                      'CreateDate': t.CreateDate.isoformat(),
                      'LastUpdateDate': t.LastUpdateDate.isoformat()
                      })

    return jsonify(row_count=row_count, page_count=page_count, page_no=page_no, page_size=page_size, data=tasks)


@main.route('/Task/QuerySingle', methods=['POST'])
def task_query_single():
    task_id = request.json['TaskId']
    tk = task.get(task_id)
    retTask = {}
    if tk:
        retTask = dict(TaskId=tk.TaskId,
                       ProjectId=tk.ProjectId,
                       TaskName=tk.TaskName,
                       TaskType=tk.TaskType,
                       Priority=tk.Priority,
                       Progress=tk.Progress,
                       AssignTo=tk.AssignTo,
                       AssignToNick=tk.AssignToProfile.Nick,
                       Status=tk.Status,
                       Effort=tk.Effort,
                       Description=tk.Description,
                       TaskLinkCase=tk.TaskLinkCase,
                       Creator=tk.CreatorProfile.Nick,
                       CreateDate=tk.CreateDate.strftime('%Y-%m-%d %H:%M'),
                       LastUpdateDate=tk.LastUpdateDate.strftime('%Y-%m-%d %H:%M')
                       )
    return jsonify(retTask=retTask)


@main.route('/Task/Create/<int:project_id>')
def task_create(project_id):
    member_list = team.member_in_project(project_id)
    return render_template('Task/Create.html', ProjectId=project_id, MemberList=member_list)


@main.route('/Task/Detail/<int:project_id>_<task_id>')
def task_detail(project_id, task_id):
    t = task.get(task_id)
    member_list = team.member_in_project(project_id)
    if t.AssignTo == g.user_id:
        t.AssignTo = -1
    return render_template('Task/Detail.html', Task=t, MemberList=member_list, CurrentUser=g.user_id)


@main.route('/Task/Update', methods=['POST'])
def task_update():
    task_id = request.json['TaskId']
    project_id = int(request.json['ProjectId'])
    task_name = request.json['TaskName']
    task_type = int(request.json['TaskType'])
    assign_to = int(request.json['AssignTo'])
    if assign_to == -1:
        assign_to = g.user_id
    priority = int(request.json['Priority'])
    progress = int(request.json['Progress'])
    status = int(request.json['Status'])
    effort = request.json['Effort']
    description = request.json['Description']
    task_link_case = request.json['TaskLinkCase']
    if task_link_case and task_link_case[-1] == ',':
        task_link_case = task_link_case[:-1]

    task.update(task_id, task_name, task_type, assign_to, priority, progress, status, effort, description,
                task_link_case)

    # ---------加日志-----------
    addLog(project_id, g.nick, ActionType.task_update,
           '<a href="/Task/Detail/%d_%s">%s</a>' % (project_id, task_id, task_id))
    # --------------------------
    return jsonify(updated=True)


@main.route('/Task/Delete', methods=['POST'])
def task_delete():
    task_id = request.json['TaskId']
    task.delete(task_id)
    # ---------加日志-----------
    addLog(0, g.nick, ActionType.task_delete, 'TaskId: %s' % task_id)
    # --------------------------
    return jsonify(deleted=True)


@main.route('/Task/CreateNew', methods=['POST'])
def task_create_new():
    project_id = int(request.json['ProjectId'])
    seq_name, next_value = util.getNext(project_id, SequenceType.Task)
    task_id = '%s_%d' % (seq_name, next_value)
    task_name = request.json['TaskName']
    task_type = int(request.json['TaskType'])
    priority = int(request.json['Priority'])
    assign_to = int(request.json['AssignTo'])
    description = request.json['Description']
    task_link_case = request.json['TaskLinkCase']

    task.create(task_id, project_id, task_name, task_type, priority, assign_to, description, task_link_case, g.user_id)
    # ---------加日志-----------
    addLog(request.json['ProjectId'], g.nick, ActionType.task_create,
           '<a href="/Task/Detail/%d_%s">%s</a>' % (project_id, task_id, task_id))
    # --------------------------
    return jsonify(created=True, ProjectId=request.json['ProjectId'])
