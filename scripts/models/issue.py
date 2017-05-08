# -*- coding: utf-8 -*-

from scripts.models.database import BaseModel
from sqlalchemy import Column, Integer, SMALLINT, String, Boolean, DateTime, Float, ForeignKey, UnicodeText
from sqlalchemy.orm import relationship
from scripts.models.userprofile import UserProfile


class IssueStatus:
    Open = 1
    Fixed = 2
    Closed = 3
    Canceled = 4


class IssueCategoryStatus:
    Enabled = 1
    Disabled = 2


class IssuePriority:
    High = 1
    Middle = 2
    Low = 3


class IssueCategory(BaseModel):
    __tablename__ = 'IssueCategory'
    CategoryId = Column('CategoryId', Integer, primary_key=True, autoincrement=True)
    CategoryName = Column('CategoryName', String(10))
    Status = Column('Status', SMALLINT)


class IssueHistory(BaseModel):
    __tablename__ = 'IssueHistory'
    HistoryId = Column('HistoryId', Integer, primary_key=True, autoincrement=True)
    IssueId = Column('IssueId', String(64), ForeignKey('Issue.IssueId'))
    RawSubject = Column('RawSubject', UnicodeText)
    NewSubject = Column('NewSubject', UnicodeText)
    RawStatus = Column('RawStatus', SMALLINT)
    NewStatus = Column('NewStatus', SMALLINT)
    RawPriority = Column('RawPriority', SMALLINT)
    NewPriority = Column('NewPriority', SMALLINT)
    RawAssignTo = Column('RawAssignTo', Integer, ForeignKey('UserProfile.UserId'))
    RawAssignToProfile = relationship('UserProfile', foreign_keys=RawAssignTo,
                                      primaryjoin=RawAssignTo == UserProfile.UserId)
    NewAssignTo = Column('NewAssignTo', Integer, ForeignKey('UserProfile.UserId'))
    NewAssignToProfile = relationship('UserProfile', foreign_keys=NewAssignTo,
                                      primaryjoin=NewAssignTo == UserProfile.UserId)
    RawCategoryId = Column('RawCategoryId', Integer, ForeignKey('IssueCategory.CategoryId'))
    RawIssueCategory = relationship('IssueCategory', foreign_keys=RawCategoryId,
                                    primaryjoin=RawCategoryId == IssueCategory.CategoryId)
    NewCategoryId = Column('NewCategoryId', Integer, ForeignKey('IssueCategory.CategoryId'))
    NewIssueCategory = relationship('IssueCategory', foreign_keys=NewCategoryId,
                                    primaryjoin=NewCategoryId == IssueCategory.CategoryId)
    RawDescription = Column('RawDescription', UnicodeText)
    NewDescription = Column('NewDescription', UnicodeText)
    Feedback = Column('Feedback', UnicodeText)
    Creator = Column('Creator', Integer, ForeignKey('UserProfile.UserId'))
    CreatorProfile = relationship('UserProfile', foreign_keys=Creator, primaryjoin=Creator == UserProfile.UserId)
    CreateDate = Column('CreateDate', DateTime)


class Issue(BaseModel):
    __tablename__ = 'Issue'
    IssueId = Column('IssueId', String(64), primary_key=True)
    ProjectId = Column('ProjectId', Integer, ForeignKey('Project.ProjectId'))
    CategoryId = Column('CategoryId', Integer, ForeignKey('IssueCategory.CategoryId'))
    Category = relationship('IssueCategory', foreign_keys=CategoryId,
                            primaryjoin=CategoryId == IssueCategory.CategoryId)
    Subject = Column('Subject', UnicodeText)
    Description = Column('Description', UnicodeText)
    Priority = Column('Priority', SMALLINT)
    Status = Column('Status', SMALLINT)
    AssignTo = Column('AssignTo', Integer, ForeignKey('UserProfile.UserId'))
    AssignToProfile = relationship('UserProfile', foreign_keys=AssignTo, primaryjoin=AssignTo == UserProfile.UserId)
    Creator = Column('Creator', Integer, ForeignKey('UserProfile.UserId'))
    CreatorProfile = relationship('UserProfile', foreign_keys=Creator, primaryjoin=Creator == UserProfile.UserId)
    CreateDate = Column('CreateDate', DateTime)
    LastUpdateDate = Column('LastUpdateDate', DateTime)
