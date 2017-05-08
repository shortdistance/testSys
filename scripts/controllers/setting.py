# -*- coding: utf-8 -*-
from flask import render_template, jsonify, request, g
from scripts.services import customfield, project
from . import bp_main as main
# 加日志
from scripts.services.log import addLog, ActionType


@main.route('/Project/Setting/<int:project_id>', methods=['GET'])
def setting_page(project_id):
    proj = project.get(project_id)
    return render_template('Setting/CustomFieldSetting.html', Project=proj)


@main.route('/Setting/QueryCustomField', methods=['POST'])
def setting_query_customfield():
    projectid = int(request.json['ProjectId'])
    retBugList, retCaseList, retTaskList = customfield.query_customfield(projectid)
    return jsonify(retBugList=retBugList, retCaseList=retCaseList, retTaskList=retTaskList)


@main.route('/Setting/EnableCustomField', methods=['POST'])
def setting_enable_customfield():
    customfieldid = int(request.json['CustomFieldId'])
    customfield.enable_customfield(customfieldid)
    # ---------加日志-----------
    addLog(0, g.nick, ActionType.setting_enable_customfield, 'FieldId: %d' % customfieldid)
    # --------------------------
    return jsonify(status='ok')


@main.route('/Setting/DisableCustomField', methods=['POST'])
def setting_disable_customfield():
    customfieldid = request.json['CustomFieldId']
    customfield.disable_customfield(customfieldid)
    # ---------加日志-----------
    addLog(0, g.nick, ActionType.setting_disable_customfield, 'FieldId: %d' % customfieldid)
    # --------------------------
    return jsonify(status='ok')


@main.route('/Setting/DeleteCustomField', methods=['POST'])
def setting_delete_customfield():
    customfieldid = request.json['CustomFieldId']
    customfield.delete_customfield(customfieldid)
    # ---------加日志-----------
    addLog(0, g.nick, ActionType.setting_delete_customfield, 'FieldId: %d' % customfieldid)
    # --------------------------
    return jsonify(status='ok')


@main.route('/Setting/SaveCustomFieldDesc', methods=['POST'])
def setting_save_field_desc():
    customfieldid = request.json['CustomFieldId']
    customfielddesc = request.json['CustomFieldDesc']
    customfield.save_customfielddesc(customfieldid, customfielddesc)

    # ---------加日志-----------
    addLog(0, g.nick, ActionType.setting_saveFieldDesc, 'FieldId: %d' % customfieldid)
    # --------------------------
    return jsonify(status='ok')


@main.route('/Setting/CreateCustomField', methods=['POST'])
def setting_create_customfield():
    projectid = int(request.json['ProjectId'])
    objectType = int(request.json['ObjectType'])
    customfieldname = request.json['CustomField']
    exist = customfield.exist_customfield(projectid, objectType, customfieldname)
    if not exist:
        customfield.create_customfield(projectid, objectType, customfieldname)

        # ---------加日志-----------
        addLog(0, g.nick, ActionType.setting_create_customfield, u'FieldName: %s' % customfieldname)
        # --------------------------
    return jsonify(status=exist)


@main.route('/Setting/EnableFieldValue', methods=['POST'])
def setting_enable_fieldvalue():
    fieldvalueid = request.json['FieldValueId']
    customfield.enable_fieldvalue(fieldvalueid)
    # ---------加日志-----------
    addLog(0, g.nick, ActionType.setting_enable_fieldvalue, 'FieldId: %d' % fieldvalueid)
    # --------------------------
    return jsonify(status='ok')


@main.route('/Setting/DisableFieldValue', methods=['POST'])
def setting_disable_fieldvalue():
    fieldvalueid = request.json['FieldValueId']
    customfield.disable_fieldvalue(fieldvalueid)
    # ---------加日志-----------
    addLog(0, g.nick, ActionType.setting_disable_fieldvalue, 'FieldId: %d' % fieldvalueid)
    # --------------------------
    return jsonify(status='ok')


@main.route('/Setting/DeleteFieldValue', methods=['POST'])
def setting_delete_fieldvalue():
    fieldvalueid = request.json['FieldValueId']
    customfield.delete_fieldvalue(fieldvalueid)
    # ---------加日志-----------
    addLog(0, g.nick, ActionType.setting_delete_fieldvalue, 'FieldId: %d' % fieldvalueid)
    # --------------------------
    return jsonify(status='ok')


@main.route('/Setting/SaveFieldValue', methods=['POST'])
def setting_save_fieldvalue():
    fieldvalueid = request.json['FieldValueId']
    fieldvalue = request.json['FieldValue']
    customfield.save_fieldvalue(fieldvalueid, fieldvalue)
    # ---------加日志-----------
    addLog(0, g.nick, ActionType.setting_save_fieldvalue, 'FieldId: %d' % fieldvalueid)
    # --------------------------
    return jsonify(status='ok')


@main.route('/Setting/CreateFieldValue', methods=['POST'])
def setting_create_fieldvalue():
    projectid = request.json['ProjectId']
    customfieldid = request.json['CustomFieldId']
    fieldvalue = request.json['FieldValue']
    exist = customfield.exist_fieldvalue(projectid, customfieldid, fieldvalue)
    if not exist:
        customfield.create_fieldvalue(projectid, customfieldid, fieldvalue)
        # ---------加日志-----------
        addLog(0, g.nick, ActionType.setting_create_fieldvalue, u'FieldValue: %s' % fieldvalue)
        # --------------------------
    return jsonify(status=exist)
