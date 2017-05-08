# -*- coding: utf-8 -*-

from datetime import datetime
import subprocess
import base64
import time

from scripts.models import database
from scripts.models.case import TestCaseResultType, \
    TestCase, TestCaseHistory, \
    TestCaseMapFieldAndValue, TestCaseLinkBug, \
    TestCaseResult, AutoRunScript, \
    ScriptPostDataField, OperType, \
    ScriptParameterBind, AutoRunHistory
from scripts.models.customfield import ObjectType, CustomField, CustomFieldValue
from scripts.models.comment import CommentType, Comment
from scripts.config import *
from sqlalchemy.orm import joinedload


def get_case_fields(projectid):
    session = database.get_session()
    customfieldlist = session.query(CustomField).filter(CustomField.ProjectId == projectid).all()
    fieldvaluelist = session.query(CustomFieldValue).filter(CustomFieldValue.ProjectId == projectid).all()
    session.close()
    retCaseSettingList = []

    d1 = {}
    for customfield in customfieldlist:
        d1 = {}
        d1['CustomFieldId'] = customfield.CustomFieldId
        d1['ObjectType'] = customfield.ObjectType
        d1['CustomFieldDesc'] = customfield.CustomFieldDesc
        d1['IsEnabled'] = customfield.IsEnabled
        d1['Show'] = True
        d1['CustomValueList'] = []
        d1['FieldValueSelected'] = ''
        for fieldvalue in fieldvaluelist:
            if fieldvalue.CustomFieldId == customfield.CustomFieldId:
                d1['CustomValueList'].append(
                    dict(CustomFieldValueId=fieldvalue.CustomFieldValueId, CustomFieldId=fieldvalue.CustomFieldId,
                         FieldValue=fieldvalue.FieldValue, IsEnabled=fieldvalue.IsEnabled, Show=True, Selected=False))
        if d1['ObjectType'] == ObjectType.TestCase:
            retCaseSettingList.append(d1)
    return retCaseSettingList


def get_case(projectid, casetype, subject, page_no):
    session = database.get_session()

    filters = []
    q = session.query(TestCase).options(joinedload(TestCase.AuthorProfile), joinedload(TestCase.LastEditByProfile),
                                        joinedload(TestCase.LastRunTesterProfile)).filter(
        TestCase.ProjectId == projectid)
    if casetype > 0:
        filters.append(TestCase.CaseType == casetype)
    if len(subject) > 0:
        filters.append(TestCase.Subject.like('%' + subject + '%'))
    for f in filters:
        q = q.filter(f)
    order_by = 'CreateTime desc'
    (row_count, page_count, page_no, page_size, data) = database.pager(q, order_by, page_no, PAGESIZE)
    session.close()
    return (row_count, page_count, page_no, page_size, data)


def get_all_case_one_time(projectid, casetype):
    session = database.get_session()
    filters = []
    if casetype == 0:
        q = session.query(TestCase).filter(TestCase.ProjectId == projectid)
    else:
        q = session.query(TestCase).filter(TestCase.ProjectId == projectid, TestCase.CaseType == casetype)
    orderby = 'CreateTime desc'
    data = q.order_by(orderby)
    session.close()
    return data


def get_one_case(case_id):
    session = database.get_session()
    caseInfo = session.query(TestCase).options(joinedload(TestCase.AuthorProfile),
                                               joinedload(TestCase.LastEditByProfile),
                                               joinedload(TestCase.LastRunTesterProfile)).filter(
        TestCase.CaseId == case_id).all()
    session.close()
    return caseInfo


def get_one_case_mapinfo(project_id, case_id):
    session = database.get_session()
    mapInfoList = session.query(TestCaseMapFieldAndValue, CustomField.CustomFieldDesc,
                                CustomFieldValue.FieldValue).join(CustomField,
                                                                  CustomField.CustomFieldId == TestCaseMapFieldAndValue.CustomFieldId).join(
        CustomFieldValue, CustomFieldValue.CustomFieldValueId == TestCaseMapFieldAndValue.CustomFieldValueId).filter(
        TestCaseMapFieldAndValue.CaseId == case_id).all()
    session.close()
    return mapInfoList


def create_testcase(caseid, projectid, casetype, subject, precondition, teststeps, expectedresult, autorunscriptfile, author):
    session = database.get_session()
    testcase = TestCase()
    testcase.CaseId = caseid
    testcase.ProjectId = projectid
    testcase.CaseType = casetype
    testcase.Subject = subject
    testcase.PreCondition = precondition
    testcase.TestSteps = teststeps
    testcase.ExpectedResult = expectedresult
    testcase.AutoRunScriptFile = autorunscriptfile
    testcase.Author = author
    create_time = datetime.now()
    testcase.CreateTime = create_time
    testcase.LastEditBy = author
    testcase.LastEditByTime = create_time
    testcase.RunFrequency = 0
    testcase.LastRunTester = author
    testcase.LastRunTime = create_time
    testcase.LastRunResult = TestCaseResultType.New_Create

    session.add(testcase)
    session.commit()
    caseid = testcase.CaseId
    session.close()
    return caseid


def create_testcase_map_field_and_value(caseid, casefieldlist):
    created = False
    for casefield in casefieldlist:
        if casefield['IsEnabled']:
            session = database.get_session()
            fieldandvalue = TestCaseMapFieldAndValue()
            fieldandvalue.CaseId = int(caseid)
            fieldandvalue.CustomFieldId = int(casefield['CustomFieldId'])
            fieldandvalue.CustomFieldValueId = int(casefield['FieldValueSelected'])

            session.add(fieldandvalue)
            session.commit()
            session.close()
            created = True
    return created


def update_testcase(caseid, projectid, subject, precondition, teststeps, expectedresult, autorunscriptfile, lasteditby,
                    Lasteditbytime):
    session = database.get_session()
    case = session.query(TestCase).filter(TestCase.CaseId == caseid).one()
    if (not case.Subject == subject) or \
            (not case.PreCondition == precondition) or \
            (not case.TestSteps == teststeps) or \
            (not case.ExpectedResult == expectedresult) or \
            (not case.AutoRunScriptFile == autorunscriptfile):
        history = TestCaseHistory()
        history.CaseId = caseid
        history.RawSubject = case.Subject
        history.NewSubject = subject
        history.RawPreCondition = case.PreCondition
        history.NewPreCondition = precondition
        history.RawTestSteps = case.TestSteps
        history.NewTestSteps = teststeps
        history.RawExpectedResult = case.ExpectedResult
        history.NewExpectedResult = expectedresult
        history.RawAutoRunScriptFile = case.AutoRunScriptFile
        history.NewAutoRunScriptFile = autorunscriptfile
        history.Creator = lasteditby
        history.CreateTime = Lasteditbytime
        session.add(history)

        case.Subject = subject
        case.PreCondition = precondition
        case.TestSteps = teststeps
        case.ExpectedResult = expectedresult
        case.AutoRunScriptFile = autorunscriptfile
        case.LastEditBy = lasteditby
        case.LastEditByTime = Lasteditbytime
        session.commit()
        session.close()
    return True


def get_change_history(case_id, page_no):
    session = database.get_session()
    q = session.query(TestCaseHistory).options(joinedload(TestCaseHistory.CreatorProfile)).filter(
        TestCaseHistory.CaseId == case_id)
    order_by = 'CreateTime desc'
    (row_count, page_count, page_no, page_size, data) = database.pager(q, order_by, page_no, PAGESIZE)
    session.close()
    return (row_count, page_count, page_no, page_size, data)


def update_case_execute_status(caseid, lastrunresult, lastruntester, lastruntime):
    session = database.get_session()
    case = session.query(TestCase).filter(TestCase.CaseId == caseid).one()
    case.RunFrequency = int(case.RunFrequency) + 1
    case.LastRunTester = lastruntester
    case.LastRunTime = lastruntime
    case.LastRunResult = lastrunresult
    session.commit()
    session.close()
    return True


def add_case_execute_history(caseid, taskid, waveid, lastrunresult, lastruntester, lastruntime, testdata, attachment,
                             backupinfo):
    session = database.get_session()
    tcResult = TestCaseResult()
    tcResult.CaseId = caseid
    tcResult.TaskId = taskid
    tcResult.WaveId = waveid
    tcResult.Tester = lastruntester
    tcResult.ExecuteTime = lastruntime
    tcResult.ExecuteResult = lastrunresult
    tcResult.TestData = testdata
    tcResult.Attachment = attachment
    tcResult.BackupInfo = backupinfo
    session.add(tcResult)
    session.commit()
    session.close()


def get_execute_history(case_id, page_no):
    session = database.get_session()
    q = session.query(TestCaseResult).options(joinedload(TestCaseResult.TesterProfile)).filter(
        TestCaseResult.CaseId == case_id)
    order_by = 'ExecuteTime desc'
    (row_count, page_count, page_no, page_size, data) = database.pager(q, order_by, page_no, PAGESIZE)
    session.close()
    return (row_count, page_count, page_no, page_size, data)


def get_execute_history_bytask(task_id):
    session = database.get_session()
    data = session.query(TestCaseResult).options(joinedload(TestCaseResult.TesterProfile)).filter(
        TestCaseResult.TaskId == task_id)
    session.close()
    return data


def delete(case_id):
    session = database.get_session()
    session.query(TestCaseHistory).filter(TestCaseHistory.CaseId == case_id).delete()
    session.query(TestCaseResult).filter(TestCaseResult.CaseId == case_id).delete()
    session.query(TestCaseMapFieldAndValue).filter(TestCaseMapFieldAndValue.CaseId == case_id).delete()
    session.query(TestCaseLinkBug).filter(TestCaseLinkBug.CaseId == case_id).delete()
    session.query(Comment).filter(Comment.CommentType == CommentType.TestCase, Comment.ObjectId == case_id).delete()
    session.query(TestCase).filter(TestCase.CaseId == case_id).delete()
    session.commit()
    session.close()


def get_case_link_bug(case_id):
    session = database.get_session()
    linkBugList = session.query(TestCaseLinkBug).options(joinedload(TestCaseLinkBug.CaseProfile),
                                                         joinedload(TestCaseLinkBug.IssueIdProfile)).filter(
        TestCaseLinkBug.CaseId == case_id).all()
    session.close()
    return linkBugList


def add_case_link_bug(case_id, issue_id):
    session = database.get_session()
    #existLink = session.query(TestCaseLinkBug).filter(TestCaseLinkBug.CaseId == case_id,TestCaseLinkBug.IssueId == issue_id).all()
    #if not existLink:
    testlinkbug = TestCaseLinkBug()
    testlinkbug.CaseId = case_id
    testlinkbug.IssueId = issue_id
    session.add(testlinkbug)
    session.commit()
    session.close()


def script_transfer(filepath, caseid):
    jarpath = UTILSPATH + '/' + 'parseXML.jar'
    # print 'java -jar "%s" --mysql %s --caseid %s  --xml "%s"' % (jarpath, DBLinkStr, caseid, filepath)
    subprocess.call('java -jar "%s" --mysql %s --caseid %s  --xml "%s"' % (jarpath, DBLinkStr, caseid, filepath),
                    shell=True)


def query_script(case_id):
    session = database.get_session()
    steplist = session.query(AutoRunScript).filter(AutoRunScript.CaseId == str(case_id)).order_by("Id asc").all()
    session.close()
    for step in steplist:
        step.Url = base64.decodestring(step.Url)
        step.Refer = base64.decodestring(step.Refer)
        step.RetData = base64.decodestring(step.RetData)
    return steplist


def query_script_retdata(caseid, stepid):
    session = database.get_session()
    data = session.query(AutoRunScript.RetData).filter(AutoRunScript.CaseId == caseid,
                                                       AutoRunScript.StepId == stepid).all()
    session.close()
    return data


def query_scipt_field(case_id):
    session = database.get_session()
    fieldlist = session.query(ScriptPostDataField).filter(ScriptPostDataField.CaseId == str(case_id)).all()
    session.close()
    for field in fieldlist:
        field.ParameterValue = base64.decodestring(field.ParameterValue)
    return fieldlist


def query_string(caseid, querystr, data):
    session = database.get_session()

    ret1 = {}
    retDataDecode = ''

    for i in data:
        if i.RetData.find(querystr) >= 0:
            ret1 = dict(Id=i.Id, StepId=i.StepId)
            break

    ret2 = session.query(ScriptPostDataField.ScriptId, ScriptPostDataField.StepId,
                         ScriptPostDataField.ParameterName).filter(
        ScriptPostDataField.CaseId == caseid,
        ScriptPostDataField.ParameterValue == base64.encodestring(querystr).strip()).all()
    session.close()

    queryRet = {}
    if ret1:
        if ret2:
            if ret1['Id'] >= ret2[0].ScriptId:
                queryRet = dict(StepId=ret2[0].StepId, OperType=OperType.ValReplace,
                                ParameterName=ret2[0].ParameterName, BackStepId=ret1['StepId'], BackParameterName='')
            else:
                queryRet = dict(StepId=ret1['StepId'], OperType=OperType.ValBind, ParameterName='',
                                BackStepId=ret2[0].StepId, BackParameterName=ret2[0].ParameterName)
        else:
            queryRet = dict(StepId=ret1['StepId'], OperType=OperType.ValBind, ParameterName='', BackStepId=0,
                            BackParameterName='')
    else:
        if ret2:
            queryRet = dict(StepId=ret2[0].StepId, OperType=OperType.ValReplace, ParameterName=ret2[0].ParameterName,
                            BackStepId=0, BackParameterName='')
        else:
            queryRet = dict(StepId=0, OperType=0, ParameterName='', BackStepId=0, BackParameterName='')

    return queryRet


def check_paramname_exist(param_name):
    session = database.get_session()
    data = session.query(ScriptParameterBind).filter(ScriptParameterBind.ParameterNameNew == param_name).all()
    session.close()
    if data:
        return False
    else:
        return True


def do_param_submit(fieldid, scriptid, stepid, caseid, opertype, paramname, paramvalue, paramtypenew, paramnamenew,
                    paramvaluenew, replaceway, isparant, bindscriptid, leftstr=None, rightstr=None):
    session = database.get_session()
    param = session.query(ScriptParameterBind).filter(ScriptParameterBind.ScriptId == scriptid).filter(
        ScriptParameterBind.StepId == stepid).filter(ScriptParameterBind.CaseId == caseid).filter(
        ScriptParameterBind.ParameterName == paramname).filter(ScriptParameterBind.ParameterValue == paramvalue).all()
    added = False
    if len(param) == 0:
        scriptbind = ScriptParameterBind()
        scriptbind.FieldId = fieldid
        scriptbind.ScriptId = scriptid
        scriptbind.StepId = stepid
        scriptbind.CaseId = caseid
        scriptbind.OperType = opertype
        scriptbind.ParameterName = paramname
        scriptbind.ParameterValue = paramvalue
        scriptbind.ParemeterTypeNew = paramtypenew
        scriptbind.ParameterNameNew = paramnamenew
        scriptbind.ParameterValueNew = paramvaluenew
        scriptbind.ReplaceWay = replaceway
        scriptbind.IsParent = isparant
        scriptbind.BindStepId = bindscriptid
        scriptbind.LefeStr = leftstr
        scriptbind.RightStr = rightstr
        session.add(scriptbind)
        session.commit()
        added = True
    session.close()
    return added


def do_cancel_param(field_id):
    session = database.get_session()
    paramlist = session.query(ScriptParameterBind).filter(ScriptParameterBind.FieldId == field_id).all()

    if len(paramlist) > 0:
        if paramlist[0].IsParent == 1:
            session.query(ScriptParameterBind).filter(
                ScriptParameterBind.ParameterNameNew == paramlist[0].ParameterNameNew).delete()
        else:
            session.query(ScriptParameterBind).filter(ScriptParameterBind.FieldId == field_id).delete()
        session.commit()
    session.close()


def query_param_bind_by_case_id(case_id):
    session = database.get_session()
    data = session.query(ScriptParameterBind).filter(ScriptParameterBind.CaseId == case_id).all()
    session.close()
    return data


def query_param_bind_by_field_id(field_id):
    session = database.get_session()
    data = session.query(ScriptParameterBind).filter(ScriptParameterBind.FieldId == field_id).all()
    session.close()
    return data


def query_bindstep_bindinfo(case_id, bind_step_id):
    session = database.get_session()
    data = session.query(ScriptParameterBind).filter(ScriptParameterBind.CaseId == case_id,
                                                     ScriptParameterBind.BindStepId == bind_step_id,
                                                     ScriptParameterBind.IsParent == 1,
                                                     ScriptParameterBind.OperType == 2,
                                                     ).all()
    session.close()
    bindinfo = []
    for i in data:
        bindinfo.append(dict(ParameterNameNew=i.ParameterNameNew,
                             ParameterValueNew=i.ParameterValueNew,
                             LefeStr=i.LefeStr,
                             RightStr=i.RightStr))
    return bindinfo


def get_postdata_and_url(case_id, step, bindparaminfo, customeparaminfo):
    session = database.get_session()
    # field
    step_field_data = session.query(ScriptPostDataField).filter(ScriptPostDataField.CaseId == str(case_id),
                                                                ScriptPostDataField.StepId == step.StepId,
                                                                ).all()
    # bind_param
    data_bind = session.query(ScriptParameterBind).filter(ScriptParameterBind.CaseId == str(case_id),
                                                          ScriptParameterBind.StepId == step.StepId
                                                          ).all()
    session.close()
    url = step.Url
    refer = step.Refer
    post_data = {}
    parametervalueold = parametervaluenew = ''
    for _p in step_field_data:
        parametervalueold = parametervaluenew = base64.decodestring(_p.ParameterValue)
        for _b in data_bind:
            if _b.FieldId == _p.Id:
                if _b.OperType == 1:
                    if _b.ParemeterTypeNew == 2:  # 随机数变量；
                        if _b.IsParent == 1:
                            parametervaluenew = '%0.f' % time.time()
                            customeparaminfo[_b.ParameterNameNew] = parametervaluenew
                        else:
                            parametervaluenew = customeparaminfo[_b.ParameterNameNew]

                    elif _b.ParemeterTypeNew == 1:  # 字符串变量；
                        parametervaluenew = _b.ParameterValueNew

                    url = url.replace('%s=%s' % (_p.ParameterName, parametervalueold),
                                      '%s=%s' % (_p.ParameterName, parametervaluenew))
                    refer = refer.replace('%s=%s' % (_p.ParameterName, parametervalueold),
                                          '%s=%s' % (_p.ParameterName, parametervaluenew))
                elif _b.OperType == 2:
                    for _n in bindparaminfo[str(_b.BindStepId)]['NeedBindParamList']:
                        if _b.ParameterNameNew == _n['ParameterNameNew'] and _n['ParameterValueNew']:
                            parametervaluenew = _n['ParameterValueNew']
                            url = url.replace('%s=%s' % (_p.ParameterName, parametervalueold),
                                              '%s=%s' % (_p.ParameterName, parametervaluenew))
                            refer = refer.replace('%s=%s' % (_p.ParameterName, parametervalueold),
                                                  '%s=%s' % (_p.ParameterName, parametervaluenew))
        if _p.ParameterType == 'PostData':
            post_data[_p.ParameterName] = parametervaluenew
    return url, refer, post_data


def insert_autorun_history(wave_id, step_id, case_id, method, url, headers, postdata, retdata, result, resultmsg,
                           creator,
                           start_time, end_time, executesec):
    session = database.get_session()
    ar_history = AutoRunHistory()
    ar_history.WaveId = wave_id
    ar_history.StepId = int(step_id)
    ar_history.CaseId = case_id
    ar_history.Method = method
    ar_history.Url = url
    ar_history.Headers = headers
    ar_history.PostData = str(postdata)
    ar_history.RetData = retdata
    ar_history.Result = int(result)
    ar_history.ResultMessage = resultmsg
    ar_history.Creator = int(creator)
    ar_history.StartTime = start_time
    ar_history.EndTime = end_time
    ar_history.ExecuteSec = executesec
    session.add(ar_history)
    session.commit()
    session.close()


def get_one_case_history_all(case_id, page_no):
    session = database.get_session()
    q = session.query(AutoRunHistory.WaveId, AutoRunHistory.CaseId).filter(
        AutoRunHistory.CaseId == case_id).distinct()
    order_by = 'Id desc'
    (row_count, page_count, page_no, page_size, data) = database.pager(q, order_by, page_no, PAGESIZE)
    session.close()
    return (row_count, page_count, page_no, page_size, data)


def get_history_by_waveid_and_caseid(wave_id, case_id):
    session = database.get_session()
    data = session.query(AutoRunHistory).options(joinedload(AutoRunHistory.CreatorProfile)).filter(
        AutoRunHistory.WaveId == wave_id, AutoRunHistory.CaseId == case_id)
    session.close()
    return data


def get_latest_wave_caseids():
    session = database.get_session()
    latest_wave = session.query(TestCaseResult).filter(TestCaseResult.WaveId != '').order_by(
        "WaveId desc").first()
    latest_wave_id = None
    data = None
    if latest_wave:
        latest_wave_id = latest_wave.WaveId
        data = session.query(TestCaseResult.CaseId).filter(TestCaseResult.WaveId == latest_wave_id)
    session.close()

    if latest_wave_id and data:
        return latest_wave_id, data
    else:
        return None, None
