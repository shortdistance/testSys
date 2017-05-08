# -*- coding: utf-8 -*-

from scripts.models.database import BaseModel
from scripts.models.userprofile import UserProfile
from scripts.models.project import Project
from sqlalchemy import Column, Integer, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Member(BaseModel):
    __tablename__ = 'Member'
    MemberId = Column('MemberId', Integer, primary_key=True, nullable=False, autoincrement=True)
    ProjectId = Column('ProjectId', Integer, ForeignKey('Project.ProjectId'))
    Project = relationship('Project', foreign_keys=ProjectId, primaryjoin=ProjectId == Project.ProjectId)
    UserId = Column('UserId', Integer, ForeignKey('UserProfile.UserId'))
    User = relationship('UserProfile', foreign_keys=UserId, primaryjoin=UserId == UserProfile.UserId)
