# -*- coding: utf-8 -*-
from scripts.models.database import BaseModel
from scripts.models.userprofile import UserProfile
from scripts.models.project import Project
from scripts.models.customfield import CustomField, CustomFieldValue
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UnicodeText
from sqlalchemy.dialects.mysql import \
    LONGTEXT, MEDIUMTEXT, TEXT

from sqlalchemy.orm import relationship
from scripts.models import Issue


class TestCaseType:
    FUNCTION = 1
    AUTO = 2


class TestCaseResultType:
    New_Create = 0
    Run_Pass = 1
    Run_Fail = 2
    Cant_Run = 3


class TestCase(BaseModel):
    __tablename__ = 'TestCase'
    CaseId = Column('CaseId', String(64), primary_key=True)
    ProjectId = Column('ProjectId', Integer, ForeignKey('Project.ProjectId'))
    ProjectProfile = relationship('Project', foreign_keys=ProjectId, primaryjoin=ProjectId == Project.ProjectId)
    CaseType = Column('CaseType', Integer)
    Subject = Column('Subject', String(255))
    PreCondition = Column('PreCondition', UnicodeText)
    TestSteps = Column('TestSteps', UnicodeText)
    ExpectedResult = Column('ExpectedResult', UnicodeText)
    AutoRunScriptFile = Column('AutoRunScriptFile', UnicodeText)
    Author = Column('Author', Integer, ForeignKey('UserProfile.UserId'))
    AuthorProfile = relationship('UserProfile', foreign_keys=Author, primaryjoin=Author == UserProfile.UserId)
    CreateTime = Column('CreateTime', DateTime)
    LastEditBy = Column('LastEditBy', Integer, ForeignKey('UserProfile.UserId'))
    LastEditByProfile = relationship('UserProfile', foreign_keys=LastEditBy,
                                     primaryjoin=LastEditBy == UserProfile.UserId)
    LastEditByTime = Column('LastEditByTime', DateTime)
    RunFrequency = Column('RunFrequency', Integer)
    LastRunTester = Column('LastRunTester', Integer, ForeignKey('UserProfile.UserId'))
    LastRunTesterProfile = relationship('UserProfile', foreign_keys=LastRunTester,
                                        primaryjoin=LastRunTester == UserProfile.UserId)
    LastRunTime = Column('LastRunTime', DateTime)
    LastRunResult = Column('LastRunResult', Integer)


class TestCaseHistory(BaseModel):
    __tablename__ = 'TestCaseHistory'
    HistoryId = Column('HistoryId', Integer, primary_key=True, autoincrement=True)
    CaseId = Column('CaseId', String(64))
    RawSubject = Column('RawSubject', String(255))
    NewSubject = Column('NewSubject', String(255))
    RawPreCondition = Column('RawPreCondition', UnicodeText)
    NewPreCondition = Column('NewPreCondition', UnicodeText)
    RawTestSteps = Column('RawTestSteps', UnicodeText)
    NewTestSteps = Column('NewTestSteps', UnicodeText)
    RawExpectedResult = Column('RawExpectedResult', UnicodeText)
    NewExpectedResult = Column('NewExpectedResult', UnicodeText)
    RawAutoRunScriptFile = Column('RawAutoRunScriptFile', UnicodeText)
    NewAutoRunScriptFile = Column('NewAutoRunScriptFile', UnicodeText)
    Creator = Column('Creator', Integer, ForeignKey('UserProfile.UserId'))
    CreatorProfile = relationship('UserProfile', foreign_keys=Creator, primaryjoin=Creator == UserProfile.UserId)
    CreateTime = Column('CreateTime', DateTime)


class TestCaseMapFieldAndValue(BaseModel):
    __tablename__ = 'TestCaseMapFieldAndValue'
    MapId = Column('MapId', Integer, primary_key=True, autoincrement=True)
    CaseId = Column('CaseId', String(64), ForeignKey('TestCase.CaseId'))
    CaseProfile = relationship('TestCase', foreign_keys=CaseId, primaryjoin=CaseId == TestCase.CaseId)
    CustomFieldId = Column('CustomFieldId', Integer, ForeignKey('CustomField.CustomFieldId'))
    FieldProfile = relationship('CustomField', foreign_keys=CustomFieldId,
                                primaryjoin=CustomFieldId == CustomField.CustomFieldId)
    CustomFieldValueId = Column('CustomFieldValueId', Integer, ForeignKey('CustomFieldValue.CustomFieldValueId'))
    FieldValueProfile = relationship('CustomFieldValue', foreign_keys=CustomFieldValueId,
                                     primaryjoin=CustomFieldValueId == CustomFieldValue.CustomFieldValueId)


class TestCaseLinkBug(BaseModel):
    __tablename__ = 'TestCaseLinkBug'
    TestCaseLinkBugId = Column('TestCaseLinkBugId', Integer, primary_key=True, autoincrement=True)
    CaseId = Column('CaseId', String(64), ForeignKey('TestCase.CaseId'))
    CaseProfile = relationship('TestCase', foreign_keys=CaseId, primaryjoin=CaseId == TestCase.CaseId)
    IssueId = Column('IssueId', String(64), ForeignKey('Issue.IssueId'))
    IssueIdProfile = relationship('Issue', foreign_keys=IssueId, primaryjoin=IssueId == Issue.IssueId)


class TestCaseResult(BaseModel):
    __tablename__ = 'TestCaseResult'
    TestCaseResultId = Column('TestCaseResultId', Integer, primary_key=True, autoincrement=True)
    CaseId = Column('CaseId', String(64), ForeignKey('TestCase.CaseId'))
    CaseProfile = relationship('TestCase', foreign_keys=CaseId, primaryjoin=CaseId == TestCase.CaseId)
    TaskId = Column('TaskId', String(64))
    WaveId = Column('WaveId', String(30))
    Tester = Column('Tester', Integer, ForeignKey('UserProfile.UserId'))
    TesterProfile = relationship('UserProfile', foreign_keys=Tester, primaryjoin=Tester == UserProfile.UserId)
    ExecuteTime = Column('ExecuteTime', DateTime)
    ExecuteResult = Column('ExecuteResult', Integer)
    TestData = Column('TestData', UnicodeText)
    Attachment = Column('Attachment', String(255))
    BackupInfo = Column('BackupInfo', UnicodeText)


class AutoRunScript(BaseModel):
    __tablename__ = 'AutoRunScript'
    Id = Column('Id', Integer, primary_key=True, autoincrement=True)
    StepId = Column('StepId', Integer)
    CaseId = Column('CaseId', String(30))
    Method = Column('Method', String(10))
    Url = Column('Url', TEXT)
    Refer = Column('Refer', TEXT)
    RetData = Column('RetData', LONGTEXT)


class ScriptPostDataField(BaseModel):
    __tablename__ = 'ScriptPostDataField'
    Id = Column('Id', Integer, primary_key=True, autoincrement=True)
    ScriptId = Column('ScriptId', Integer)
    StepId = Column('StepId', Integer)
    CaseId = Column('CaseId', String(30))
    Method = Column('Method', String(10))
    ParameterType = Column('ParameterType', String(30))
    ParameterName = Column('ParameterName', UnicodeText)
    ParameterValue = Column('ParameterValue', MEDIUMTEXT)


class OperType:
    ValReplace = 1
    ValBind = 2
    InsertFun = 3


class ScriptParameterBind(BaseModel):
    __tablename__ = 'ScriptParameterBind'
    Id = Column('Id', Integer, primary_key=True, autoincrement=True)
    FieldId = Column('FieldId', Integer)
    ScriptId = Column('ScriptId', Integer)
    StepId = Column('StepId', Integer)
    CaseId = Column('CaseId', String(30))
    OperType = Column('OperType', Integer)  # {ValReplace: 1, ValBind: 2, InsertFun: 3}
    ParameterName = Column('ParameterName', UnicodeText)
    ParameterValue = Column('ParameterValue', UnicodeText)
    ParemeterTypeNew = Column('ParemeterTypeNew', Integer)  # {StringVal: 1, TimeStamp: 2}
    ParameterNameNew = Column('ParameterNameNew', UnicodeText)
    ParameterValueNew = Column('ParameterValueNew', UnicodeText)
    IsParent = Column('IsParent', Integer)
    ReplaceWay = Column('ReplaceWay', Integer)  # {All:1,  CurrItem:2}
    BindStepId = Column('BindStepId', Integer)
    LefeStr = Column('LefeStr', UnicodeText)
    RightStr = Column('RightStr', UnicodeText)


class AutoRunHistory(BaseModel):
    __tablename__ = 'AutoRunHistory'
    Id = Column('Id', Integer, primary_key=True, autoincrement=True)
    WaveId = Column('WaveId', String(30))
    StepId = Column('StepId', Integer)
    CaseId = Column('CaseId', String(30))
    Method = Column('Method', String(10))
    Url = Column('Url', TEXT)
    Headers = Column('Headers', TEXT)
    PostData = Column('PostData', MEDIUMTEXT)
    RetData = Column('RetData', LONGTEXT)
    Result = Column('Result', Integer)
    ResultMessage = Column('ResultMessage', String(64))
    Creator = Column('Creator', Integer, ForeignKey('UserProfile.UserId'))
    CreatorProfile = relationship('UserProfile', foreign_keys=Creator, primaryjoin=Creator == UserProfile.UserId)
    StartTime = Column('StartTime', DateTime)
    EndTime = Column('EndTime', DateTime)
    ExecuteSec = Column('ExecuteSec', Integer)
