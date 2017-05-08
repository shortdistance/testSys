# -*- coding: utf-8 -*-
from flask import render_template, request, g, jsonify, send_from_directory
from scripts.models.util import SequenceType
from scripts.services import team, issue, case, util
from scripts.config import *
from . import bp_main as main
# 加日志
from scripts.services.log import addLog, ActionType


@main.route('/Project/Issue/<int:project_id>')
def issue_list(project_id):
    member_list = team.member_in_project(project_id)
    category = issue.available_category()
    return render_template('Issue/List.html', ProjectId=project_id, MemberList=member_list,
                           Category=category)


@main.route('/Issue/Create/<int:project_id>')
def issue_create_page(project_id):
    member_list = team.member_in_project(project_id)
    category = issue.available_category()
    return render_template('Issue/Create.html', ProjectId=project_id, MemberList=member_list, Category=category)


@main.route('/Issue/CreateNew', methods=['POST'])
def issue_create_new():
    project_id = request.json['ProjectId']
    seq_name, next_value = util.getNext(project_id, SequenceType.Issue)
    issue_id = '%s_%d' % (seq_name, next_value)
    subject = u'%s' % request.json['Subject']
    priority = request.json['Priority']
    assign_to = request.json['AssignTo']
    description = u'%s' % request.json['Description']
    category_id = request.json['CategoryId']
    issue_id = issue.create(issue_id, project_id, category_id, subject, priority, assign_to, description, g.user_id)
    # ---------加日志-----------
    addLog(request.json['ProjectId'], g.nick, ActionType.issue_create,
           '<a href="/Issue/Detail/%d_%s">%s</a>' % (project_id, issue_id, issue_id))
    # --------------------------
    return jsonify(created=True, ProjectId=project_id, IssueId=issue_id)


@main.route('/Issue/CreateNewAndLink', methods=['POST'])
def issue_create_new_and_link():
    case_id = request.json['CaseId']
    project_id = request.json['ProjectId']
    seq_name, next_value = util.getNext(project_id, SequenceType.Issue)
    issue_id = '%s_%d' % (seq_name, next_value)
    subject = u'%s' % request.json['Subject']
    priority = request.json['Priority']
    assign_to = request.json['AssignTo']
    description = u'%s' % request.json['Description']
    category_id = request.json['CategoryId']

    issue_id = issue.create(issue_id, project_id, category_id, subject, priority, assign_to, description, g.user_id)
    # ---------加日志-----------
    addLog(request.json['ProjectId'], g.nick, ActionType.issue_create,
           '<a href="/Issue/Detail/%d_%s">%s</a>' % (project_id, issue_id, issue_id))
    # --------------------------
    case.add_case_link_bug(case_id, issue_id)
    return jsonify(created=True, ProjectId=project_id, IssueId=issue_id)


@main.route('/Issue/Query', methods=['POST'])
def issue_query():
    projectid = int(request.json['ProjectId'])
    subject = request.json['Subject']
    assign_to = int(request.json['AssignTo'])
    if assign_to == -1:
        assign_to = g.user_id
    category_id = int(request.json['CategoryId'])
    status_open = request.json['Open']
    status_fixed = request.json['Fixed']
    status_closed = request.json['Closed']
    status_canceled = request.json['Canceled']
    page_no = int(request.json['PageNo'])
    (row_count, page_count, page_no, page_size, data) = issue.query(projectid, subject, assign_to, category_id,
                                                                    status_open, status_fixed, status_closed,
                                                                    status_canceled, 'IssueId desc', page_no)
    issue_list = []
    for i in data.all():
        issue_list.append(
            {'IssueId': i.IssueId, 'ProjectId': i.ProjectId, 'Category': i.Category.CategoryName, 'Subject': i.Subject,
             'Priority': i.Priority, 'Status': i.Status, 'AssignTo': i.AssignToProfile.Nick,
             'Creator': i.CreatorProfile.Nick, 'LastUpdateDate': i.LastUpdateDate.isoformat()})
    return jsonify(row_count=row_count, page_count=page_count, page_no=page_no, page_size=page_size, data=issue_list)


@main.route('/Issue/Detail/<int:projectid>_<issue_id>')
def issue_detail(projectid, issue_id):
    iss = issue.get(issue_id)
    member_list = team.member_in_project(projectid)
    category = issue.available_category()
    if iss.AssignTo == g.user_id:
        iss.AssignTo = -1
    history_list = issue.get_history(issue_id)
    return render_template('Issue/Detail.html', Issue=iss, HistoryList=history_list,
                           MemberList=member_list, Category=category, CurrentUser=g.user_id)


@main.route('/Issue/Update', methods=['POST'])
def issue_update():
    issueid = request.json['IssueId']
    subject = request.json['Subject']
    assign_to = request.json['AssignTo']
    if int(assign_to) == -1:
        assign_to = g.user_id
    priority = request.json['Priority']
    category_id = request.json['CategoryId']
    status = request.json['Status']
    description = request.json['Description']
    issue.update(issueid, subject, category_id, assign_to, priority, status, description, g.user_id)
    # ---------加日志-----------
    addLog(0, g.nick, ActionType.issue_update, '%s' % issueid)
    # --------------------------
    return jsonify(updated=True)


@main.route('/Issue/Delete', methods=['POST'])
def issue_delete():
    issueid = request.json['IssueId']
    issue.delete(issueid)
    # ---------加日志-----------
    addLog(0, g.nick, ActionType.issue_delete, 'IssueId: %s' % issueid)
    # --------------------------
    return jsonify(deleted=True)


@main.route('/Issue/Export/<int:project_id>', methods=['GET'])
def issue_export(project_id):
    filename = issue.ExportToExcel(project_id)
    return send_from_directory(ISSUE_ATTACHMENT_UPLOAD_PATH, filename)


@main.route('/Issue/Import/<int:project_id>', methods=['GET'])
def issue_import(project_id):
    return render_template('Issue/Import.html', ProjectId=project_id)
