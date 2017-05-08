# -*- coding: utf-8 -*-
from scripts.models.database import BaseModel
from sqlalchemy import Column, Integer, SMALLINT, String, Boolean, DateTime, Float, ForeignKey


class UserStatus:
    Enabled = 1
    Disabled = 2


class UserProfile(BaseModel):
    __tablename__ = 'UserProfile'
    UserId = Column('UserId', Integer, primary_key=True, autoincrement=True)
    Email = Column('Email', String(255), unique=True)
    Nick = Column('Nick', String(16))
    Password = Column('Password', String(128))
    Status = Column('Status', SMALLINT)
    IsAdmin = Column('IsAdmin', Boolean)
    RegDate = Column('RegDate', DateTime)
