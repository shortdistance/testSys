# -*- coding: utf-8 -*-
from scripts.models.database import BaseModel
from scripts.models.project import Project, ProjectStatus
from sqlalchemy import Column, Integer, SMALLINT, String, Boolean, DateTime, Float, ForeignKey, UnicodeText
from sqlalchemy.orm import relationship


class ObjectType:
    Bug = 1
    TestCase = 2
    Task = 3
    Team = 4
    Other = 5


class CustomField(BaseModel):
    __tablename__ = 'CustomField'
    CustomFieldId = Column('CustomFieldId', Integer, primary_key=True, autoincrement=True)
    ProjectId = Column('ProjectId', Integer, ForeignKey('Project.ProjectId'))
    ProjectProfile = relationship('Project', foreign_keys=ProjectId, primaryjoin=ProjectId == Project.ProjectId)
    ObjectType = Column('ObjectType', SMALLINT)
    CustomFieldDesc = Column('CustomFieldDesc', String(32))
    IsEnabled = Column('IsEnabled', Boolean)
    CustomFieldValues = relationship('CustomFieldValue')


class CustomFieldValue(BaseModel):
    __tablename__ = 'CustomFieldValue'
    CustomFieldValueId = Column('CustomFieldValueId', Integer, primary_key=True, autoincrement=True)
    ProjectId = Column('ProjectId', Integer, ForeignKey('Project.ProjectId'))
    ProjectProfile = relationship('Project', foreign_keys=ProjectId, primaryjoin=ProjectId == Project.ProjectId)
    CustomFieldId = Column('CustomFieldId', Integer, ForeignKey('CustomField.CustomFieldId'))
    CustomFieldProfile = relationship('CustomField', foreign_keys=CustomFieldId,
                                      primaryjoin=CustomFieldId == CustomField.CustomFieldId)
    FieldValue = Column('FieldValue', UnicodeText)
    IsEnabled = Column('IsEnabled', Boolean)
