# -*- coding: utf-8 -*-
from scripts.models.database import BaseModel
from sqlalchemy import Column, Integer, String


class SequenceType:
    Case = 1
    Task = 2
    Issue = 3


class Sequence(BaseModel):
    __tablename__ = 'Sequence'
    Name = Column('Name', String(32), primary_key=True)
    Type = Column('Type', Integer, default=1)
    ProjectId = Column('ProjectId', Integer, default=0)
    CurrentValue = Column('CurrentValue', Integer, default=0)
    Increment = Column('Increment', Integer, default=1)
