# -*- coding: utf-8 -*-

from scripts.models.database import BaseModel
from scripts.models.userprofile import UserProfile

from sqlalchemy import Column, Integer, SMALLINT, String, DateTime, Float, ForeignKey, UnicodeText
from sqlalchemy.orm import relationship

# 1: 高
# 2: 中
# 3：低
class TaskPriority:
    High = 1
    Middle = 2
    Low = 3


# 1: 新建
# 2: 进行中
# 3：完成
# 4：取消
class TaskStatus:
    New = 1
    InProgress = 2
    Completed = 3
    Canceled = 4


# 1: 普通
# 2: 测试
class TaskType:
    Default = 1
    Test_Manual = 2
    Test_Auto = 3


class Task(BaseModel):
    __tablename__ = 'Task'
    TaskId = Column('TaskId', String(64), primary_key=True)
    ProjectId = Column('ProjectId', Integer, ForeignKey('Project.ProjectId'))
    TaskName = Column('TaskName', String(48))
    TaskType = Column('TaskType', SMALLINT)
    Priority = Column('Priority', SMALLINT)
    Progress = Column('Progress', SMALLINT)
    AssignTo = Column('AssignTo', Integer, ForeignKey('UserProfile.UserId'))
    AssignToProfile = relationship('UserProfile', foreign_keys=AssignTo, primaryjoin=AssignTo == UserProfile.UserId)
    Status = Column('Status', SMALLINT)
    Effort = Column('Effort', Float)
    Description = Column('Description', UnicodeText)
    TaskLinkCase = Column('TaskLinkCase', UnicodeText)
    Creator = Column('Creator', Integer, ForeignKey('UserProfile.UserId'))
    CreatorProfile = relationship('UserProfile', foreign_keys=Creator, primaryjoin=Creator == UserProfile.UserId)
    CreateDate = Column('CreateDate', DateTime)
    LastUpdateDate = Column('LastUpdateDate', DateTime)
