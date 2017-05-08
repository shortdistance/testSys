# -*- coding: utf-8 -*-
from scripts.models.database import BaseModel
from sqlalchemy import Column, Integer, SMALLINT, String, Boolean, DateTime, Float, ForeignKey, UnicodeText
from sqlalchemy.orm import relationship


class HostMonitor(BaseModel):
    __tablename__ = 'HostMonitor'
    Id = Column('Id', Integer, primary_key=True, autoincrement=True)
    Host = Column('Host', String(64))
    CpuIdel = Column('CpuIdel', Integer)
    MemFree = Column('MemFree', Integer)
    CreateTime = Column('CreateTime', DateTime)
