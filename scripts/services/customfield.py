# -*- coding: utf-8 -*-

from scripts.models import database
from scripts.models.customfield import ObjectType, CustomField, CustomFieldValue
from scripts.config import *
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import func


def query_customfield(projectid):
    session = database.get_session()
    customfieldlist = session.query(CustomField).filter(CustomField.ProjectId == projectid).all()
    fieldvaluelist = session.query(CustomFieldValue).filter(CustomFieldValue.ProjectId == projectid,
                                                            CustomField.CustomFieldId == CustomFieldValue.CustomFieldId).all()
    session.close()
    retBugList = []
    retCaseList = []
    retTaskList = []

    d1 = {}
    for customfield in customfieldlist:
        d1 = {}
        d1['CustomFieldId'] = customfield.CustomFieldId
        d1['ProjectId'] = customfield.ProjectId
        d1['ObjectType'] = customfield.ObjectType
        d1['CustomFieldDesc'] = customfield.CustomFieldDesc
        d1['IsEnabled'] = customfield.IsEnabled
        d1['Show'] = True
        d1['CustomValueList'] = []
        for fieldvalue in fieldvaluelist:
            if fieldvalue.CustomFieldId == customfield.CustomFieldId:
                d1['CustomValueList'].append(
                    dict(CustomFieldValueId=fieldvalue.CustomFieldValueId, CustomFieldId=fieldvalue.CustomFieldId,
                         FieldValue=fieldvalue.FieldValue, IsEnabled=fieldvalue.IsEnabled, Show=True))
        if d1['ObjectType'] == ObjectType.Bug:
            retBugList.append(d1)
        elif d1['ObjectType'] == ObjectType.TestCase:
            retCaseList.append(d1)
        elif d1['ObjectType'] == ObjectType.Task:
            retTaskList.append(d1)
    return retBugList, retCaseList, retTaskList


def query_case_customfield(projectid, objecttype):
    session = database.get_session()
    customfieldlist = session.query(CustomField).filter(CustomField.ProjectId == projectid,
                                                        CustomField.ObjectType == objecttype).all()
    fieldvaluelist = session.query(CustomFieldValue).filter(CustomFieldValue.ProjectId == projectid,
                                                            CustomField.CustomFieldId == CustomFieldValue.CustomFieldId,
                                                            CustomField.ObjectType == objecttype).all()
    session.close()
    retList = []

    d1 = {}
    for customfield in customfieldlist:
        d1 = {}
        d1['CustomFieldId'] = customfield.CustomFieldId
        d1['ProjectId'] = customfield.ProjectId
        d1['ObjectType'] = customfield.ObjectType
        d1['CustomFieldDesc'] = customfield.CustomFieldDesc
        d1['IsEnabled'] = customfield.IsEnabled
        d1['Show'] = True
        d1['CustomValueList'] = []
        for fieldvalue in fieldvaluelist:
            if fieldvalue.CustomFieldId == customfield.CustomFieldId:
                d1['CustomValueList'].append(
                    dict(CustomFieldValueId=fieldvalue.CustomFieldValueId, CustomFieldId=fieldvalue.CustomFieldId,
                         FieldValue=fieldvalue.FieldValue, IsEnabled=fieldvalue.IsEnabled, Show=True))
        if d1['ObjectType'] == objecttype:
            retList.append(d1)
    return retList


def exist_customfield(projectid, objecttype, customfieldname):
    session = database.get_session()
    customfield = session.query(CustomField).filter(CustomField.ProjectId == projectid,
                                                    CustomField.ObjectType == objecttype,
                                                    CustomField.CustomFieldDesc == customfieldname).first()
    if customfield:
        return True
    else:
        return False


def create_customfield(projectid, objecttype, customfielddesc):
    session = database.get_session()
    if exist_customfield(projectid, objecttype, customfielddesc.strip()):
        pass
    else:
        customfield = CustomField()
        customfield.ProjectId = projectid
        customfield.ObjectType = objecttype
        customfield.CustomFieldDesc = customfielddesc.strip()
        customfield.IsEnabled = True
        session.add(customfield)
        session.commit()
        session.close()


def enable_customfield(customfieldid):
    session = database.get_session()
    session.query(CustomField).filter(CustomField.CustomFieldId == customfieldid).update({'IsEnabled': True})
    session.commit()
    session.close()


def disable_customfield(customfieldid):
    session = database.get_session()
    session.query(CustomField).filter(CustomField.CustomFieldId == customfieldid).update({'IsEnabled': False})
    session.commit()
    session.close()


def delete_customfield(customfieldid):
    session = database.get_session()
    session.query(CustomField).filter(CustomField.CustomFieldId == customfieldid).delete()
    session.query(CustomFieldValue).filter(CustomFieldValue.CustomFieldId == customfieldid).delete()
    session.commit()
    session.close()


def save_customfielddesc(customfieldid, customfielddesc):
    session = database.get_session()
    session.query(CustomField).filter(CustomField.CustomFieldId == customfieldid).update(
        {'CustomFieldDesc': customfielddesc})
    session.commit()
    session.close()


def exist_fieldvalue(projectid, customfieldid, fieldvalue):
    session = database.get_session()
    fieldvalue = session.query(CustomFieldValue).filter(CustomFieldValue.ProjectId == projectid,
                                                        CustomFieldValue.CustomFieldId == customfieldid,
                                                        CustomFieldValue.FieldValue == fieldvalue).first()
    if fieldvalue:
        return True
    else:
        return False


def create_fieldvalue(projectid, customfieldid, fieldvalue):
    session = database.get_session()
    if exist_fieldvalue(projectid, customfieldid, fieldvalue):
        pass
    else:
        customfieldvalue = CustomFieldValue()
        customfieldvalue.CustomFieldId = customfieldid
        customfieldvalue.ProjectId = projectid
        customfieldvalue.FieldValue = fieldvalue.strip()
        customfieldvalue.IsEnabled = True

        session.add(customfieldvalue)
        session.commit()
        session.close()


def enable_fieldvalue(fieldvalueid):
    session = database.get_session()
    session.query(CustomFieldValue).filter(CustomFieldValue.CustomFieldValueId == fieldvalueid).update(
        {'IsEnabled': True})
    session.commit()
    session.close()


def disable_fieldvalue(fieldvalueid):
    session = database.get_session()
    session.query(CustomFieldValue).filter(CustomFieldValue.CustomFieldValueId == fieldvalueid).update(
        {'IsEnabled': False})
    session.commit()
    session.close()


def delete_fieldvalue(fieldvalueid):
    session = database.get_session()
    session.query(CustomFieldValue).filter(CustomFieldValue.CustomFieldValueId == fieldvalueid).delete()
    session.commit()
    session.close()


def save_fieldvalue(fieldvalueid, fieldvalue):
    session = database.get_session()
    session.query(CustomFieldValue).filter(CustomFieldValue.CustomFieldValueId == fieldvalueid).update(
        {'FieldValue': fieldvalue})
    session.commit()
    session.close()
