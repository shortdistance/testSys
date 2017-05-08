# -*- coding: utf-8 -*-
from flask import request, g, jsonify
from scripts.services import comment
from scripts.models.log import ActionType
from . import bp_main as main
# 加日志
from scripts.services import log


@main.route('/Comment/Create', methods=['POST'])
def createIssueComment():
    comment_type = int(request.json['CommentType'])
    object_id = request.json['ObjectId']
    content = request.json['Content']

    comment.createComment(comment_type, object_id, g.user_id, content)
    # ---------加日志-----------
    log.addLog(0, g.nick, ActionType.comment_createComment, content)
    # --------------------------
    return jsonify(createcomment=True)


@main.route('/Comment/Query', methods=['POST'])
def queryIssueComment():
    comment_type = int(request.json['CommentType'])
    object_id = request.json['ObjectId']
    page_no = request.json['PageNo']
    (row_count, page_count, page_no, page_size, data) = comment.queryComment(comment_type, object_id, page_no)
    commentList = []
    for i in data.all():
        commentList.append(
            {'CommentId': i.Comment.CommentId, 'CommentType': i.Comment.CommentType, 'ObjectId': i.Comment.ObjectId,
             'Author': i.Comment.Author, 'AuthorName': i.UserProfile.Nick,
             'CreateTime': i.Comment.CreateTime.strftime('%Y-%m-%d %H:%M:%S'), 'Content': (i.Comment.Content)})
    return jsonify(row_count=row_count, page_count=page_count, page_no=page_no, page_size=page_size,
                   commentList=commentList)
