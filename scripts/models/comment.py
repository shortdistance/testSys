# -*- coding: utf-8 -*-
from scripts.models.database import BaseModel
from sqlalchemy import Column, Integer, SMALLINT, String, Boolean, DateTime, Float, ForeignKey


class CommentType:
    Bug = 1
    TestCase = 2


class Comment(BaseModel):
    __tablename__ = 'Comment'
    CommentId = Column('CommentId', Integer, primary_key=True, autoincrement=True)
    CommentType = Column('CommentType', SMALLINT)
    ObjectId = Column('ObjectId', String(64))
    Author = Column('Author', Integer)
    CreateTime = Column('CreateTime', DateTime)
    Content = Column('Content', String(256))
