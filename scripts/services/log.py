# -*- coding: utf-8 -*-
from scripts.models import database
from scripts.models.log import ActionType, JsonActionTypeDetailList, ActionLog
from datetime import datetime
from scripts.config import PAGESIZE
from sqlalchemy.sql.expression import func, or_, not_
from scripts.config import *


def get_action_desc_by_opcode(opcode, username, detail=''):
    retStr = ''
    for i in JsonActionTypeDetailList:
        if opcode == i['op_code']:
            if detail == '':
                retStr = (i['op_detail'] % username)
            else:
                retStr = (i['op_detail'] % (username, detail))

        else:
            continue
    return retStr


def addLog(project_id, username, opcode, detail=''):
    session = database.get_session()
    actionlog = ActionLog()
    actionlog.ProjectId = int(project_id)
    actionlog.UserName = str(username)
    actionlog.ActionType = str(opcode)
    actionlog.CreateTime = datetime.now()
    actionlog.ActionDetail = u'%s' % get_action_desc_by_opcode(opcode, username, detail)
    session.add(actionlog)
    session.commit()
    session.close()


def getlog(page_no):
    session = database.get_session()
    q = session.query(ActionLog)
    order_by = 'CreateTime desc'
    (row_count, page_count, page_no, page_size, data) = database.pager(q, order_by, page_no, PAGESIZE)

    session.close()
    return (row_count, page_count, page_no, page_size, data)
