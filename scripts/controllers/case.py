# -*- coding: utf-8 -*-
from datetime import datetime
import sys, base64
from flask import render_template, request, g, jsonify
from scripts.models.util import SequenceType
from scripts.services import team, case, task, util
from . import bp_main as main
# 日志
from scripts.services.log import addLog, ActionType


@main.route('/Project/Case/<int:project_id>', methods=['GET'])
def case_list(project_id):
    member_list = team.member_in_project(project_id)
    # return 'hello world!!'
    return render_template('Case/List.html', MemberList=member_list, ProjectId=project_id)


@main.route('/Case/Query', methods=['POST'])
def case_query():
    project_id = int(request.json['ProjectId'])
    case_type = int(request.json['CaseType'])
    subject = request.json['Subject']
    page_no = int(request.json['PageNo'])

    (row_count, page_count, page_no, page_size, data) = case.get_case(project_id, case_type, subject, page_no)
    caselist = []
    for i in data.all():
        caselist.append({'CaseId': i.CaseId,
                         'ProjectId': i.ProjectId,
                         'CaseType': i.CaseType,
                         'Subject': i.Subject,
                         'PreCondition': i.PreCondition,
                         'TestSteps': i.TestSteps,
                         'ExpectedResult': i.ExpectedResult,
                         'AutoRunScriptFile': i.AutoRunScriptFile,
                         'Author': i.AuthorProfile.Nick,
                         'CreateTime': i.CreateTime.strftime('%Y-%m-%d %H:%M'),
                         'LastEditBy': i.LastEditByProfile.Nick,
                         'LastEditByTime': i.LastEditByTime.strftime('%Y-%m-%d %H:%M'),
                         'RunFrequency': i.RunFrequency,
                         'LastRunTester': i.LastRunTesterProfile.Nick,
                         'LastRunTime': i.LastRunTime.strftime('%Y-%m-%d %H:%M'),
                         'LastRunResult': i.LastRunResult})
    return jsonify(row_count=row_count, page_count=page_count, page_no=page_no, page_size=page_size, caselist=caselist)


@main.route('/Case/TaskQueryCase', methods=['POST'])
def case_query_all():
    projectid = int(request.json['ProjectId'])
    casetype = int(request.json['CaseType'])
    taskid = request.json['TaskId']

    t = task.get(taskid)
    linkcase = t.TaskLinkCase.split(',')
    data = case.get_all_case_one_time(projectid, casetype)
    caselist = []
    for i in data.all():
        if unicode(i.CaseId) in linkcase:
            caselist.append(dict(CaseId=i.CaseId,
                                 TaskId=taskid,
                                 WaveId='',
                                 CaseType=casetype,
                                 Subject=i.Subject,
                                 PreCondition=i.PreCondition,
                                 TestSteps=i.TestSteps,
                                 ExpectedResult=i.ExpectedResult,
                                 AutoRunScriptFile=i.AutoRunScriptFile,
                                 IsChecked=True,
                                 IsExecuteSucc=False,
                                 IsExecuteFail=False,
                                 IsCantExecute=False,
                                 IsNeedCreateBug=False,
                                 NotExecutePass=False,
                                 Result=0,
                                 IssueAssignTo=0,
                                 TestData='',
                                 Attachment='',
                                 BackupInfo=''))
        else:
            caselist.append(dict(CaseId=i.CaseId,
                                 TaskId='',
                                 WaveId='',
                                 CaseType=casetype,
                                 Subject=i.Subject,
                                 PreCondition='',
                                 TestSteps='',
                                 ExpectedResult='',
                                 AutoRunScriptFile='',
                                 IsChecked=False,
                                 IsExecuteSucc=False,
                                 IsExecuteFail=False,
                                 IsCantExecute=False,
                                 IsNeedCreateBug=False,
                                 NotExecutePass=False,
                                 Result=0,
                                 IssueAssignTo=0,
                                 TestData='',
                                 Attachment='',
                                 BackupInfo=''))
    data = case.get_execute_history_bytask(taskid)
    for j in data.all():
        for mycase in caselist:
            if mycase['IsChecked'] == True and mycase['CaseId'] == j.CaseId:
                mycase['Result'] = j.ExecuteResult
    return jsonify(caselist=caselist)


@main.route('/Case/Update', methods=['POST'])
def case_update():
    caseid = request.json['CaseId']
    projectid = int(request.json['ProjectId'])
    subject = request.json['Subject']
    precondition = request.json['PreCondition']
    teststeps = request.json['TestSteps']
    expectedresult = request.json['ExpectedResult']
    autorunscriptfile = request.json['AutoRunScriptFile']
    lasteditby = g.user_id
    lasteditbytime = datetime.now()
    case.update_testcase(caseid, projectid, subject, precondition, teststeps, expectedresult, autorunscriptfile,
                         lasteditby, lasteditbytime)
    # ---------添加日志-----------
    addLog(0, g.nick, ActionType.case_update, '<a href="/Case/Detail/%d_%s">%s</a>' % (projectid, caseid, caseid))
    # --------------------------
    return jsonify(updated=True)


@main.route('/Case/Execute', methods=['POST'])
def case_execute():
    caseid = request.json['CaseId']
    taskid = request.json['TaskId']
    waveid = request.json['WaveId']
    lastrunresult = int(request.json['Result'])
    lastruntester = g.user_id
    lastruntime = datetime.now()
    testdata = request.json['TestData']
    attachment = request.json['Attachment']
    backupinfo = request.json['BackupInfo']
    case.update_case_execute_status(caseid, lastrunresult, lastruntester, lastruntime)
    case.add_case_execute_history(caseid, taskid, waveid, lastrunresult, lastruntester, lastruntime, testdata,
                                  attachment, backupinfo)
    # ---------添加日志-----------
    addLog(0, g.nick, ActionType.case_execute, '%s' % caseid)
    # ----------------------------
    return jsonify(executed=True)


@main.route('/Case/Delete', methods=['POST'])
def case_delete():
    caseid = request.json['CaseId']
    case.delete(caseid)
    # ---------添加日志-----------
    addLog(0, g.nick, ActionType.case_delete, '%s' % caseid)
    # --------------------------
    return jsonify(deleted=True)


@main.route('/CaseField/Query', methods=['POST'])
def case_query_fields():
    projectid = int(request.json['ProjectId'])
    casefieldslist = case.get_case_fields(projectid)
    return jsonify(casefieldslist=casefieldslist)


@main.route('/Case/Create/<int:project_id>')
def case_create_page(project_id):
    member_list = team.member_in_project(project_id)
    return render_template('Case/Create.html', ProjectId=project_id, MemberList=member_list)


@main.route('/Case/CreateNew', methods=['POST'])
def case_create_new():
    project_id = int(request.json['ProjectId'])
    seq_name, next_value = util.getNext(project_id, SequenceType.Case)
    case_id = '%s_%d' % (seq_name, next_value)
    case_type = int(request.json['CaseType'])
    subject = u'%s' % request.json['Subject']
    precondition = u'%s' % request.json['Precondition']
    test_steps = u'%s' % request.json['TestSteps']
    expected_result = u'%s' % request.json['ExpectedResult']
    case_field_list = request.json['CaseFieldList']
    auto_run_script_file = request.json['AutoRunScriptFile']

    case.create_testcase(case_id, project_id, case_type, subject, precondition, test_steps, expected_result,
                         auto_run_script_file, g.user_id)
    # ---------添加日志-----------
    addLog(0, g.nick, ActionType.case_create, '<a href="/Case/Detail/%d_%s">%s</a>' % (project_id, case_id, case_id))
    # ----------------------------
    if case_field_list:
        case.create_testcase_map_field_and_value(case_id, case_field_list)
    return jsonify(created=True)


@main.route('/Case/Detail/<int:project_id>_<case_id>', methods=['GET'])
def query_case_detail(project_id, case_id):
    caseInfo = case.get_one_case(case_id)
    retTCInfo = {}
    if caseInfo:
        retTCInfo = dict(CaseId=caseInfo[0].CaseId,
                         ProjectId=caseInfo[0].ProjectId,
                         CaseType=caseInfo[0].CaseType,
                         Subject=caseInfo[0].Subject,
                         PreCondition=caseInfo[0].PreCondition,
                         TestSteps=caseInfo[0].TestSteps,
                         ExpectedResult=caseInfo[0].ExpectedResult,
                         AutoRunScriptFile=caseInfo[0].AutoRunScriptFile,
                         Author=caseInfo[0].AuthorProfile.Nick,
                         CreateTime=caseInfo[0].CreateTime,
                         LastEditBy=caseInfo[0].LastEditByProfile.Nick,
                         LastEditByTime=caseInfo[0].LastEditByTime,
                         RunFrequency=caseInfo[0].RunFrequency,
                         LastRunTester=caseInfo[0].LastRunTesterProfile.Nick,
                         LastRunTime=caseInfo[0].LastRunTime,
                         LastRunResult=caseInfo[0].LastRunResult
                         )
    return render_template('Case/Detail.html', RetTCInfo=retTCInfo, ProjectId=project_id, Current_User=g.nick)


@main.route('/Case/ChangeHistory', methods=['POST'])
def query_case_change_history():
    case_id = request.json['CaseId']
    page_no = int(request.json['PageNo'])
    (row_count, page_count, page_no, page_size, data) = case.get_change_history(case_id, page_no)
    change_history_list = []
    for i in data.all():
        change_history_list.append({'HistoryId': i.HistoryId,
                                    'CaseId': i.CaseId,
                                    'RawSubject': i.RawSubject,
                                    'NewSubject': i.NewSubject,
                                    'RawPreCondition': i.RawPreCondition,
                                    'NewPreCondition': i.NewPreCondition,
                                    'RawTestSteps': i.RawTestSteps,
                                    'NewTestSteps': i.NewTestSteps,
                                    'RawExpectedResult': i.RawExpectedResult,
                                    'NewExpectedResult': i.NewExpectedResult,
                                    'RawAutoRunScriptFile': i.RawAutoRunScriptFile,
                                    'NewAutoRunScriptFile': i.NewAutoRunScriptFile,
                                    'Creator': i.CreatorProfile.Nick,
                                    'CreateTime': i.CreateTime.strftime('%Y-%m-%d %H:%M')})
    return jsonify(row_count=row_count, page_count=page_count, page_no=page_no, page_size=page_size,
                   change_history_list=change_history_list)


@main.route('/Case/ExecuteHistory', methods=['POST'])
def query_case_execute_history():
    case_id = request.json['CaseId']
    page_no = int(request.json['PageNo'])
    (row_count, page_count, page_no, page_size, data) = case.get_execute_history(case_id, page_no)
    execute_history_list = []
    for i in data.all():
        execute_history_list.append({'TestCaseResultId': i.TestCaseResultId,
                                     'CaseId': i.CaseId,
                                     'Tester': i.TesterProfile.Nick,
                                     'ExecuteTime': i.ExecuteTime.strftime('%Y-%m-%d %H:%M'),
                                     'ExecuteResult': i.ExecuteResult,
                                     'TestData': i.TestData,
                                     'Attachment': i.Attachment,
                                     'BackupInfo': i.BackupInfo})
    return jsonify(row_count=row_count, page_count=page_count, page_no=page_no, page_size=page_size,
                   execute_history_list=execute_history_list)


@main.route('/Case/GetExistingFields', methods=['POST'])
def case_get_existing_fields():
    project_id = int(request.json['ProjectId'])
    case_id = request.json['CaseId']
    mapInfoList = case.get_one_case_mapinfo(project_id, case_id)
    caseSettingList = []
    caseSettingList = case.get_case_fields(project_id)
    for caseSetting in caseSettingList:
        for mapinfo in mapInfoList:
            if caseSetting['CustomFieldId'] == mapinfo[0].CustomFieldId:
                caseSetting['FieldValueSelected'] = mapinfo[2]
                for fieldSetting in caseSetting['CustomValueList']:
                    if fieldSetting['CustomFieldValueId'] == mapinfo[0].CustomFieldValueId:
                        fieldSetting['Selected'] = True
    return jsonify(CaseSettingList=caseSettingList)


@main.route('/Case/GetLinkBug', methods=['POST'])
def case_get_link_bug():
    case_id = request.json['CaseId']
    linkBugList = case.get_case_link_bug(case_id)
    retLinkBugList = []
    for link_bug in linkBugList:
        retLinkBugList.append(
            dict(CaseId=case_id, IssueId=link_bug.IssueId, IssueSubject=link_bug.IssueIdProfile.Subject,
                 IssueStatus=link_bug.IssueIdProfile.Status))
    return jsonify(retLinkBugList=retLinkBugList)


@main.route('/Case/Script/<int:project_id>_<case_id>', methods=['GET'])
def case_edit_script_page(project_id, case_id):
    return render_template('Case/ScriptEdit.html', ProjectId=project_id, CaseId=case_id)


@main.route('/Case/Script/Query', methods=['POST'])
def case_script_query():
    case_id = request.json['CaseId']
    data = case.query_script(case_id)
    postdatalist = case.query_scipt_field(case_id)
    parambindlist = case.query_param_bind_by_case_id(case_id)

    reload(sys)
    sys.setdefaultencoding('utf-8')
    steplist = []
    fieldlist = []
    parambinddict = {}
    isparambind = False

    for step in data:
        fieldlist = []
        for field in postdatalist:
            if field.ScriptId == step.Id and field.StepId == step.StepId:
                parambinddict = {}
                isparambind = False
                for parambind in parambindlist:
                    if parambind.StepId == field.StepId and parambind.ScriptId == field.ScriptId and parambind.FieldId == field.Id:
                        isparambind = True
                        parambinddict = dict(OperType=parambind.OperType,
                                             ParameterName=parambind.ParameterName,
                                             ParameterValue=parambind.ParameterValue,
                                             ParemeterTypeNew=parambind.ParemeterTypeNew,
                                             ParameterNameNew=parambind.ParameterNameNew,
                                             ParameterValueNew=parambind.ParameterValueNew,
                                             ReplaceWay=parambind.ReplaceWay,
                                             IsParent=parambind.IsParent,
                                             BindStepId=parambind.BindStepId,
                                             LefeStr=parambind.LefeStr,
                                             RightStr=parambind.RightStr)

                queryret = dict(StepId=0, OperType=0, ParameterName='', BackStepId=0, BackParameterName='')
                if field.ParameterValue and field.ParameterValue not in ['null', 'false']:
                    queryret = case.query_string(case_id, field.ParameterValue, data)
                fieldlist.append(dict(Id=field.Id,
                                      ParameterType=field.ParameterType,
                                      ParameterName=field.ParameterName,
                                      ParameterValue=field.ParameterValue,
                                      ParamBind=parambinddict,
                                      IsParamBind=isparambind,
                                      QueryRet=queryret))
        steplist.append(dict(Id=str(step.Id),
                             StepId=str(step.StepId),
                             CaseId=step.CaseId,
                             Method=step.Method,
                             Url=step.Url,
                             Parameter=fieldlist,
                             RetDataShow=False,
                             RetData='',
                             RetDataSize=len(step.RetData)
                             ))

    return jsonify(steplist=steplist)


@main.route('/Case/Script/QueryScriptRetData', methods=['POST'])
def case_script_query_ret_data():
    case_id = request.json['CaseId']
    step_id = int(request.json['StepId'])
    ret_data_list = case.query_script_retdata(case_id, step_id)

    ret_data_show = False
    ret_data_decoded = ''
    if len(ret_data_list) > 0:
        ret_data_show = True
        ret_data_decoded = base64.decodestring(ret_data_list[0][0])
    return jsonify(retdatashow=ret_data_show, retdata=ret_data_decoded)


@main.route('/Case/Script/QueryField', methods=['POST'])
def case_script_query_field():
    field_id = int(request.json['FieldId'])
    param_bind_list = case.query_param_bind_by_field_id(field_id)
    param_bind_dict = {}
    is_param_bind = False
    if len(param_bind_list) > 0:
        is_param_bind = True
        param_bind_dict = dict(OperType=param_bind_list[0].OperType,
                               ParameterName=param_bind_list[0].ParameterName,
                               ParameterValue=param_bind_list[0].ParameterValue,
                               ParemeterTypeNew=param_bind_list[0].ParemeterTypeNew,
                               ParameterNameNew=param_bind_list[0].ParameterNameNew,
                               ParameterValueNew=param_bind_list[0].ParameterValueNew,
                               ReplaceWay=param_bind_list[0].ReplaceWay,
                               IsParent=param_bind_list[0].IsParent,
                               BindStepId=param_bind_list[0].BindStepId,
                               LefeStr=param_bind_list[0].LefeStr,
                               RightStr=param_bind_list[0].RightStr)
    return jsonify(isparambind=is_param_bind, parambinddict=param_bind_dict)


@main.route('/Case/Script/QueryString', methods=['POST'])
def case_script_string_query():
    case_id = request.json['CaseId']
    query_str = request.json['Query_String']
    data = case.query_script(case_id)
    query_ret = case.query_string(case_id, query_str, data)
    return jsonify(querysucc=True, queryret=query_ret)


@main.route('/Case/Script/CheckNewParamName', methods=['POST'])
def case_script_check_new_param_name():
    param_name = request.json['ParamName']
    checked = case.check_paramname_exist(param_name)
    return jsonify(checked=checked)


@main.route('/Case/Script/DoParamSubmit', methods=['POST'])
def case_script_do_param_submit():
    field_id = int(request.json['FieldId'])
    script_id = int(request.json['ScriptId'])
    step_id = int(request.json['StepId'])
    case_id = request.json['CaseId']
    oper_type = int(request.json['OperType'])
    parameter_name = request.json['ParameterName']
    parameter_value = request.json['ParameterValue']
    parameter_type_new = int(request.json['ParemeterTypeNew'])
    parameter_name_new = request.json['ParameterNameNew']
    parameter_value_new = request.json['ParameterValueNew']
    replace_way = int(request.json['ReplaceWay'])
    is_parent = int(request.json['IsParent'])
    bind_scriptid = int(request.json['BindStepId'])
    left_str = request.json['LefeStr']
    right_str = request.json['RightStr']
    added = case.do_param_submit(field_id, script_id, step_id, case_id, oper_type, parameter_name,
                                 parameter_value, parameter_type_new, parameter_name_new, parameter_value_new,
                                 replace_way, is_parent, bind_scriptid, left_str, right_str)

    if replace_way == 1:
        post_data_list = case.query_scipt_field(case_id)
        for field in post_data_list:
            if field.StepId >= step_id:
                if field.ParameterValue == parameter_value:
                    case.do_param_submit(field.Id, field.ScriptId, field.StepId, field.CaseId, oper_type,
                                         field.ParameterName,
                                         parameter_value, parameter_type_new, parameter_name_new,
                                         parameter_value_new,
                                         replace_way, 0, bind_scriptid, left_str, right_str)
    return jsonify(added=added)


@main.route('/Case/Script/CancelParam', methods=['POST'])
def case_script_do_cancel_param():
    field_id = int(request.json['FieldId'])
    case.do_cancel_param(field_id)
    return jsonify(canceled=True)
