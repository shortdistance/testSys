# -*- coding: utf-8 -*-

from scripts.models.database import BaseModel

from sqlalchemy import Column, Integer, SMALLINT, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship


class ProjectStatus:
    InProgress = 1
    Completed = 2
    Canceled = 3


class Project(BaseModel):
    __tablename__ = 'Project'
    ProjectId = Column('ProjectId', Integer, primary_key=True, autoincrement=True)
    ProjectName = Column('ProjectName', String(30))
    ProjectPrefix = Column('ProjectPrefix', String(5))
    Status = Column('Status', SMALLINT)
    Progress = Column('Progress', SMALLINT)
    Creator = Column('Creator', Integer, ForeignKey('UserProfile.UserId'))
    UserProfile = relationship("UserProfile")
    CreateDate = Column('CreateDate', DateTime)
    LastUpdateDate = Column('LastUpdateDate', DateTime)
    Members = relationship("Member")
    ProjectAdmin = Column('ProjectAdmin', SMALLINT, default=0)

