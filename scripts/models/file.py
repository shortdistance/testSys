# -*- coding: utf-8 -*-

from scripts.models.database import BaseModel
from sqlalchemy import Column, Integer, SMALLINT, String, Boolean, DateTime, Float, ForeignKey, UnicodeText


class ObjectType:
    Bug = 1
    TestCase = 2


class FileUpload(BaseModel):
    __tablename__ = 'FileUpload'
    FileId = Column('FileId', Integer, primary_key=True, autoincrement=True)
    PathName = Column('PathName', String(256))
    Extension = Column('Extension', String(30))
    Size = Column('Size', Integer)
    ObjectType = Column('ObjectType', SMALLINT)
    Author = Column('Author', Integer)
    CreateTime = Column('CreateTime', DateTime)
