# -*- coding: utf-8 -*-
from scripts.models import database
from scripts.models import CommentType, Comment, UserProfile, UserStatus
from datetime import datetime
from scripts.config import PAGESIZE
from sqlalchemy.sql.expression import func, or_, not_
from scripts.config import *


def queryComment(comment_type, object_id, page_no):
    session = database.get_session()
    q = session.query(Comment, UserProfile).filter(Comment.CommentType == comment_type, Comment.ObjectId == object_id,
                                                   Comment.Author == UserProfile.UserId)
    order_by = 'CreateTime desc'
    (row_count, page_count, page_no, page_size, data) = database.pager(q, order_by, page_no, PAGESIZE)
    session.close()
    return (row_count, page_count, page_no, page_size, data)


def createComment(comment_type, object_id, author, content):
    session = database.get_session()
    comment = Comment()
    comment.CommentType = comment_type
    comment.ObjectId = object_id
    comment.Author = author
    comment.CreateTime = datetime.now()
    comment.Content = content

    session.add(comment)
    session.commit()
    session.close()
