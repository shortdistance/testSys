# -*- coding: utf-8 -*-
from flask import request, send_from_directory
from scripts.services import issue, case
from scripts.config import *
from . import bp_main as main
import os, uuid


@main.route('/case/upload_attachment/<int:project_id>', methods=['POST'])
def upload_case_file(project_id):
    file = request.files['attachment']
    ext = file.filename.split('.')[-1]
    filename = str(uuid.uuid4()) + '.' + ext
    parentdir = CASE_ATTACHMENT_UPLOAD_PATH + '/' + str(project_id)
    if not os.path.exists(parentdir):
        os.makedirs(parentdir)
    filepath = os.path.join(parentdir, filename)
    file.save(filepath)
    fileurl = 'http://%s:%d/case/upload_attachment/%s/%s' % (HOST, PORT, project_id, filename)
    return fileurl


@main.route('/case/upload_autorun/<int:project_id>_<int:case_id>', methods=['POST'])
def upload_autorun_file(project_id, case_id):
    file = request.files['attachment1']
    ext = file.filename.split('.')[-1]
    if ext.lower() != 'xml':
        return u'文件格式不正确, 脚本原文件格式为xml!'
    filename = str(uuid.uuid4()) + '.' + ext
    parentdir = CASE_AUTORUN_UPLOAD_PATH + '/' + str(project_id)
    if not os.path.exists(parentdir):
        os.makedirs(parentdir)
    filepath = os.path.join(parentdir, filename)
    file.save(filepath)
    fileurl = 'http://%s:%d/case/upload_autorun/%s/%s' % (HOST, PORT, project_id, filename)

    jarpath = UTILSPATH + '/' + 'parseXML.jar'
    case.script_transfer(filepath, str(case_id))
    return fileurl


@main.route('/task/upload_attachment/<int:project_id>', methods=['POST'])
def upload_task_file(project_id):
    file = request.files['attachment']
    ext = file.filename.split('.')[-1]
    filename = str(uuid.uuid4()) + '.' + ext
    parentdir = TASK_ATTACHMENT_UPLOAD_PATH + '/' + str(project_id)
    if not os.path.exists(parentdir):
        os.makedirs(parentdir)
    filepath = os.path.join(parentdir, filename)
    file.save(filepath)
    fileurl = 'http://%s:%d/task/upload_attachment/%s/%s' % (HOST, PORT, project_id, filename)
    return fileurl


@main.route('/issue/upload_attachment/<int:project_id>', methods=['POST'])
def upload_issue_file(project_id):
    file = request.files['attachment']
    ext = file.filename.split('.')[-1]
    filename = str(uuid.uuid4()) + '.' + ext
    parentdir = ISSUE_ATTACHMENT_UPLOAD_PATH + '/' + str(project_id)
    if not os.path.exists(parentdir):
        os.makedirs(parentdir)
    filepath = os.path.join(parentdir, filename)
    file.save(filepath)
    fileurl = 'http://%s:%d/issue/upload_attachment/%s/%s' % (HOST, PORT, project_id, filename)
    return fileurl


@main.route('/issue/import/<int:project_id>', methods=['POST'])
def upload_issue_import(project_id):
    file = request.files['fileToUpload']
    ext = file.filename.split('.')[-1]
    if ext not in ['xls', 'xlsx']:
        return u'文件格式不正确, Excel文件格式为xls,xlsx!'

    filename = str(uuid.uuid4()) + '.' + ext
    parentdir = ISSUE_IMPORT_UPLOAD_PATH + '/' + str(project_id)
    if not os.path.exists(parentdir):
        os.makedirs(parentdir)
    filepath = os.path.join(parentdir, filename)
    file.save(filepath)
    fileurl = 'http://%s:%d/issue/import/%s/%s' % (HOST, PORT, project_id, filename)
    issue.ImportToDB(project_id, filepath)
    return fileurl


@main.route('/case/upload_attachment/<int:projectid>/<filename>', methods=['GET'])
def get_case_upload_attachment(projectid, filename):
    parentdir = CASE_ATTACHMENT_UPLOAD_PATH + '/' + str(projectid)
    return send_from_directory(parentdir, filename)


@main.route('/case/upload_autorun/<int:projectid>/<filename>', methods=['GET'])
def get_case_upload_autorun(projectid, filename):
    parentdir = CASE_AUTORUN_UPLOAD_PATH + '/' + str(projectid)
    return send_from_directory(parentdir, filename)


@main.route('/task/upload_attachment/<int:projectid>/<filename>', methods=['GET'])
def get_task_upload_attachment(projectid, filename):
    parentdir = TASK_ATTACHMENT_UPLOAD_PATH + '/' + str(projectid)
    return send_from_directory(parentdir, filename)


@main.route('/issue/upload_attachment/<int:projectid>/<filename>', methods=['GET'])
def get_issue_upload_attachment(projectid, filename):
    parentdir = ISSUE_ATTACHMENT_UPLOAD_PATH + '/' + str(projectid)
    return send_from_directory(parentdir, filename)


@main.route('/issue/import/<int:projectid>/<filename>', methods=['GET'])
def upload_get_issue_import(projectid, filename):
    parentdir = ISSUE_IMPORT_UPLOAD_PATH + '/' + str(projectid)
    return send_from_directory(parentdir, filename)
