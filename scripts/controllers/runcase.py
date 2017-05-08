# -*- coding: utf-8 -*-
from datetime import datetime
import time
import requests
from flask import request, jsonify
from scripts.models.case import TestCaseResultType
from scripts.services import case
from scripts.ext.http import httpRequest
from scripts.ext.utils import myString
from . import bp_main as main

"""
paraminfo =
{
    '1': {
        'NeedBindParamList': [
            {
                'ParameterNameNew': ,
                'ParameterValueNew': ,
                'LefeStr': ,
                'RightStr':
            },
            {
                'ParameterNameNew': ,
                'ParameterValueNew': ,
                'LefeStr': ,
                'RightStr':
            }
        ]
    }
}
"""


@main.route('/RunCase', methods=['POST'])
def run_case():
    wave_id = str(request.json['WaveId'])
    case_id = str(request.json['CaseId'])
    creator = int(request.json['UserId'])

    steplist = case.query_script(case_id)

    # 存放绑定变量
    bindparaminfo = {}
    # 存放自动发生变化的参数化变量;
    customeparaminfo = {}

    headers = {}
    strheaders = ''
    postdata = {}
    status_code = -1
    retmsg = ''
    content = ''
    isPass = True
    laststepid = 0

    http_session = requests.Session()
    for step in steplist:
        # 记录开始时间
        start_dt = datetime.now()
        start_time = time.time()
        # 分析绑定信息
        bindparaminfo[str(step.StepId)] = {}
        bindparaminfo[str(step.StepId)]['NeedBindParamList'] = []
        bindparaminfo[str(step.StepId)]['NeedBindParamList'] = case.query_bindstep_bindinfo(case_id,
                                                                                            step.StepId)
        # 获取postdata, 参数化Url
        postdata = {}

        step.Url, step.Refer, postdata = case.get_postdata_and_url(case_id, step, bindparaminfo,
                                                                   customeparaminfo)
        # 发送报文
        headers = {}
        if step.Refer:
            headers = {
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
                'Connection': 'Keep-Alive', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept-Encoding': 'gzip, deflate', 'Refer': step.Refer}
        status_code, retmsg, content = run_case_send(http_session, step.Url, headers, step.Method, postdata,
                                                     bindparaminfo[str(step.StepId)]['NeedBindParamList'])
        # 记录结束时间和耗时
        end_dt = datetime.now()
        end_time = time.time()
        executesec = end_time - start_time
        # 插入执行记录到历史表
        content = unicode(content).replace('\'', '\\\'')
        strheaders = unicode(headers).replace('\'', '\\\'')
        case.insert_autorun_history(wave_id, step.StepId, case_id, step.Method, step.Url, strheaders, postdata,
                                    content,
                                    status_code, retmsg, creator,
                                    start_dt, end_dt, executesec)
        # 如果返回码异常就停止执行
        laststepid = step.StepId
        if status_code != 200:
            isPass = False
            break
    http_session.close()

    lastrunresult = TestCaseResultType.New_Create
    if isPass:
        lastrunresult = TestCaseResultType.Run_Pass
    else:
        lastrunresult = TestCaseResultType.Run_Fail

    lastruntester = creator
    lastruntime = datetime.now()
    case.update_case_execute_status(case_id, lastrunresult, creator, lastruntime)
    return jsonify(isPass=isPass, lastStepId=laststepid, retCode=status_code, retMsg=content)


"""
    needbindparamlist = [
        {
            'ParameterNameNew': ,
            'ParameterValueNew': ,
            'LefeStr': ,
            'RightStr':
        },
    ]
"""


def run_case_send(session, url, headers, method, postdata, needbindparamlist):
    status_code = -1
    retmsg = ''
    content = ''

    if method == 'POST':
        status_code, content = httpRequest.Post_S(session, url, postdata, headers)
    elif method == 'GET':
        status_code, content = httpRequest.Get_S(session, url, headers)

    if status_code == 200:
        if needbindparamlist:
            for needbindparam in needbindparamlist:
                retmsg, needbindparam['ParameterValueNew'] = myString.GetMidStr(content, needbindparam['LefeStr'],
                                                                                needbindparam['RightStr'])
                if needbindparam['ParameterValueNew'] is None:
                    status_code = -2
                    break
    return status_code, retmsg, content


@main.route('/RunCase/GetOneCaseHistory', methods=['POST'])
def run_case_get_case_history_all():
    case_id = request.json['CaseId']
    page_no = int(request.json['PageNo'])
    (row_count, page_count, page_no, page_size, data) = case.get_one_case_history_all(case_id, page_no)
    wave_info_all = []
    wave_info = []
    wave_info_new = []
    IsPass = True
    RetCode = 200
    Runner = ''
    for i in data.all():
        IsPass = True
        RetCode = 200
        Runner = ''
        wave_info = []
        wave_info_new = []
        wave_info = case.get_history_by_waveid_and_caseid(i.WaveId, case_id)
        for j in wave_info.all():
            if j.Result != 200:
                IsPass = False
                RetCode = j.Result
            Runner = j.CreatorProfile.Nick
            wave_info_new.append(dict(
                WaveId=j.WaveId,
                StepId=j.StepId,
                CaseId=j.CaseId,
                Method=j.Method,
                Url='/' + '/'.join(j.Url.split('://')[1].split('/')[1:]),
                Headers=j.Headers,
                PostData=j.PostData,
                RetData=j.RetData,
                Result=j.Result,
                ResultMessage=j.ResultMessage,
                Runner=j.CreatorProfile.Nick,
                StartTime=j.StartTime.strftime('%Y-%m-%d %H:%M:%S'),
                EndTime=j.EndTime.strftime('%Y-%m-%d %H:%M:%S'),
                ExecuteSec=j.ExecuteSec
            ))
        wave_info_all.append(dict(
            WaveId=i.WaveId,
            WaveInfo=wave_info_new,
            IsPass=IsPass,
            RetCode=RetCode,
            Runner=Runner
        ))
    return jsonify(row_count=row_count, page_count=page_count, page_no=page_no, page_size=page_size,
                   wave_info_all=wave_info_all)


@main.route('/RunCase/GetHistoryByWaveIdAndCaseId', methods=['POST'])
def run_case_get_history_by_waveid_and_caseid():
    wave_id = str(request.json['WaveId'])
    case_id = str(request.json['CaseId'])
    data = case.get_history_by_waveid_and_caseid(wave_id, case_id)
    wave_info = []
    for i in data.all():
        wave_info.append({
            'WaveId': i.WaveId,
            'StepId': i.StepId,
            'CaseId': i.CaseId,
            'Method': i.Method,
            'Url': '/' + '/'.join(i.Url.split('://')[1].split('/')[1:]),
            'Headers': i.Headers,
            'PostData': i.PostData,
            'RetData': i.RetData,
            'Result': i.Result,
            'ResultMessage': i.ResultMessage,
            'Creator': i.CreatorProfile.Nick,
            'StartTime': i.StartTime.strftime('%Y-%m-%d %H:%M:%S'),
            'EndTime': i.EndTime.strftime('%Y-%m-%d %H:%M:%S'),
            'ExecuteSec': i.ExecuteSec
        })
    return jsonify(wave_info=wave_info)


@main.route('/RunCase/GetLatestWaveHistory', methods=['POST'])
def run_case_get_latest_wave_history():
    latest_wave_id, ret_data = case.get_latest_wave_caseids()
    ret_wave_info = []

    if latest_wave_id and ret_data:
        for j in ret_data.all():
            wave_info = []
            IsPass = True
            RetCode = 200
            Runner = ''

            ret_runcase = case.get_history_by_waveid_and_caseid(latest_wave_id, j.CaseId)
            for i in ret_runcase.all():
                if i.Result != 200:
                    IsPass = False
                    RetCode = i.Result
                Runner = i.CreatorProfile.Nick
                wave_info.append(dict(
                    WaveId=i.WaveId,
                    StepId=i.StepId,
                    CaseId=i.CaseId,
                    Method=i.Method,
                    Url='/' + '/'.join(i.Url.split('://')[1].split('/')[1:]),
                    Headers=i.Headers,
                    PostData=i.PostData,
                    RetData=i.RetData,
                    Result=i.Result,
                    ResultMessage=i.ResultMessage,
                    Creator=i.CreatorProfile.Nick,
                    StartTime=i.StartTime.strftime('%Y-%m-%d %H:%M:%S'),
                    EndTime=i.EndTime.strftime('%Y-%m-%d %H:%M:%S'),
                    ExecuteSec=i.ExecuteSec
                ))
            ret_wave_info.append(dict(
                WaveId=latest_wave_id,
                CaseId=j.CaseId,
                IsPass=IsPass,
                RetCode=RetCode,
                Runner=Runner,
                WaveInfo=wave_info
            ))
    return jsonify(latest_wave_id=latest_wave_id, ret_wave_info=ret_wave_info)
