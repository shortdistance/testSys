# -*- coding: utf-8 -*-

from datetime import datetime
import uuid

import xlrd
import xlwt

from scripts.models import database
from scripts.models.case import TestCaseLinkBug
from scripts.models.issue import IssueStatus, IssueCategoryStatus, IssuePriority, IssueCategory, IssueHistory, \
    Issue
from scripts.models.userprofile import UserProfile
from scripts.models.comment import CommentType, Comment
from scripts.config import *
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from scripts.services import userprofile


def create(issue_id, project_id, category_id, subject, priority, assign_to, description, creator):
    session = database.get_session()
    issue = Issue()
    issue.IssueId = issue_id
    issue.ProjectId = project_id
    issue.CategoryId = category_id
    issue.Subject = subject.strip()
    issue.Description = description
    issue.Priority = priority
    issue.Status = IssueStatus.Open
    if int(assign_to) == -1:
        issue.AssignTo = creator
    else:
        issue.AssignTo = assign_to
    issue.Creator = creator
    issue.CreateDate = datetime.now()
    issue.LastUpdateDate = datetime.now()
    session.add(issue)
    session.commit()
    issueid = issue.IssueId
    session.close()
    return issueid


def available_category():
    session = database.get_session()
    data = session.query(IssueCategory).filter(IssueCategory.Status == IssueCategoryStatus.Enabled).all()
    session.close()
    return data


def all_category():
    session = database.get_session()
    data = session.query(IssueCategory).all()
    session.close()
    return data


def query(projectid, subject, assign_to, category_id, status_open, status_fixed, status_closed, status_canceled,
          order_by, page_no):
    session = database.get_session()

    filters = []
    status = []
    projectid = int(projectid)
    subject = subject.strip()
    if projectid > 0:
        filters.append(Issue.ProjectId == projectid)
    if len(subject) > 0:
        filters.append(Issue.Subject.like('%' + subject + '%'))
    if not assign_to == 0:
        filters.append(Issue.AssignTo == assign_to)
    if not category_id == -1:
        filters.append(Issue.CategoryId == category_id)
    if status_open:
        status.append(IssueStatus.Open)
    if status_fixed:
        status.append(IssueStatus.Fixed)
    if status_closed:
        status.append(IssueStatus.Closed)
    if status_canceled:
        status.append(IssueStatus.Canceled)
    if len(status) > 0:
        filters.append(Issue.Status.in_(status))

    q = session.query(Issue).join(UserProfile, UserProfile.UserId == Issue.Creator).join(UserProfile,
                                                                                         UserProfile.UserId == Issue.AssignTo)
    for f in filters:
        q = q.filter(f)
    order_by =  'CreateDate desc'
    (row_count, page_count, page_no, page_size, data) = database.pager(q, order_by, page_no, PAGESIZE)
    session.close()
    return (row_count, page_count, page_no, page_size, data)


def export_all_case(project_id):
    session = database.get_session()
    data = session.query(Issue).options(joinedload(Issue.CreatorProfile), joinedload(Issue.AssignToProfile),
                                        joinedload(Issue.Category)).filter(Issue.ProjectId == project_id).all()
    session.close()
    return data


def get(issue_id):
    session = database.get_session()
    issue = session.query(Issue).options(joinedload(Issue.CreatorProfile), joinedload(Issue.AssignToProfile),
                                         joinedload(Issue.Category)).filter(Issue.IssueId == issue_id).one()
    session.close()
    return issue


def get_history(issue_id):
    session = database.get_session()
    history_list = session.query(IssueHistory).options(joinedload(IssueHistory.RawAssignToProfile),
                                                       joinedload(IssueHistory.NewAssignToProfile),
                                                       joinedload(IssueHistory.CreatorProfile),
                                                       joinedload(IssueHistory.RawIssueCategory),
                                                       joinedload(IssueHistory.NewIssueCategory)).filter(
        IssueHistory.IssueId == issue_id).order_by(IssueHistory.CreateDate.desc())
    session.close()
    return history_list


def update(issue_id, subject, category_id, assign_to, priority, status, description, current_user):
    session = database.get_session()
    subject = subject.strip()
    issue = session.query(Issue).filter(Issue.IssueId == issue_id).one()
    changeAssignTo = not (issue.AssignTo == assign_to)
    if (not issue.Subject == subject) or (not issue.CategoryId == category_id) or (not issue.Status == status) or (
            not issue.Priority == priority) or (not issue.AssignTo == assign_to) or (
            not issue.Description == description):
        history = IssueHistory()
        history.IssueId = issue.IssueId
        history.RawSubject = issue.Subject
        history.NewSubject = subject
        history.RawStatus = issue.Status
        history.NewStatus = status
        history.RawPriority = issue.Priority
        history.NewPriority = priority
        history.RawAssignTo = issue.AssignTo
        history.NewAssignTo = assign_to
        history.RawCategoryId = issue.CategoryId
        history.NewCategoryId = category_id
        history.Feedback = current_user
        history.RawDescription = issue.Description
        history.NewDescription = description
        history.Creator = current_user
        history.CreateDate = datetime.now()
        session.add(history)

        issue.Subject = subject
        issue.CategoryId = category_id
        issue.AssignTo = assign_to
        issue.Priority = priority
        issue.Status = status
        issue.Description = description
        issue.LastUpdateDate = datetime.now()

        session.commit()
        session.close()
    return True


def delete(issue_id):
    session = database.get_session()
    session.query(IssueHistory).filter(IssueHistory.IssueId == issue_id).delete()
    session.query(Comment).filter(Comment.CommentType == CommentType.Bug, Comment.ObjectId == issue_id).delete()
    session.query(TestCaseLinkBug).filter(TestCaseLinkBug.IssueId == issue_id).delete()
    session.query(Issue).filter(Issue.IssueId == issue_id).delete()
    session.commit()
    session.close()


def statistics(project_id):
    session = database.get_session()
    issue_status = session.query(Issue.Status, func.count(Issue.Status)).filter(Issue.ProjectId == project_id).group_by(
        Issue.Status).all()
    issue_priority = session.query(Issue.Priority, func.count(Issue.Priority)).filter(
        Issue.ProjectId == project_id).group_by(Issue.Priority).all()
    session.commit()
    session.close()
    return (issue_status, issue_priority)


def enable_category(categoryid):
    session = database.get_session()
    user = session.query(IssueCategory).filter(IssueCategory.CategoryId == categoryid).update(
        {'Status': IssueCategoryStatus.Enabled})
    session.commit()
    session.close()


def disable_category(categoryid):
    session = database.get_session()
    user = session.query(IssueCategory).filter(IssueCategory.CategoryId == categoryid).update(
        {'Status': IssueCategoryStatus.Disabled})
    session.commit()
    session.close()


def delete_category(categoryid):
    session = database.get_session()
    user = session.query(IssueCategory).filter(IssueCategory.CategoryId == categoryid).delete()
    session.commit()
    session.close()


def create_category(categoryname):
    session = database.get_session()
    c = IssueCategory()
    c.CategoryName = categoryname.strip()
    c.Status = IssueCategoryStatus.Enabled
    session.add(c)
    session.commit()
    session.close()


def exist_category(categoryname):
    session = database.get_session()
    c = session.query(IssueCategory).filter(IssueCategory.CategoryName == categoryname).count()
    session.close()
    return c > 0


def ExportToExcel(project_id):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('Sheet1')
    sheet.write(0, 0, u'编号')
    sheet.write(0, 1, u'项目编号')
    sheet.write(0, 2, u'类别')
    sheet.write(0, 3, u'标题')
    sheet.write(0, 4, u'描述')
    sheet.write(0, 5, u'优先级')
    sheet.write(0, 6, u'状态')
    sheet.write(0, 7, u'处理人')
    sheet.write(0, 8, u'创建人')
    sheet.write(0, 9, u'创建时间')
    sheet.write(0, 10, u'最近更新时间')
    issuelist = export_all_case(project_id)
    rowlen = len(issuelist)
    for i in range(rowlen):
        sheet.write(i + 1, 0, issuelist[i].IssueId)
        sheet.write(i + 1, 1, issuelist[i].ProjectId)
        sheet.write(i + 1, 2, issuelist[i].Category.CategoryName)
        sheet.write(i + 1, 3, issuelist[i].Subject)
        sheet.write(i + 1, 4, issuelist[i].Description)
        sheet.write(i + 1, 5, getPriorityNameByKey(issuelist[i].Priority))
        sheet.write(i + 1, 6, getStatusNameByKey(issuelist[i].Status))
        sheet.write(i + 1, 7, issuelist[i].CreatorProfile.Nick)
        sheet.write(i + 1, 8, issuelist[i].AssignToProfile.Nick)
        sheet.write(i + 1, 9, issuelist[i].CreateDate.strftime('%Y-%m-%d %H:%M:%S'))
        sheet.write(i + 1, 10, issuelist[i].LastUpdateDate.strftime('%Y-%m-%d %H:%M:%S'))
    if not os.path.exists(ISSUE_ATTACHMENT_UPLOAD_PATH):
        os.makedirs(ISSUE_ATTACHMENT_UPLOAD_PATH)
    filename = str(uuid.uuid4()) + '.xls'
    filepath = os.path.join(ISSUE_ATTACHMENT_UPLOAD_PATH, filename)
    wbk.save(filepath)
    return filename


def getPriorityNameByKey(priorityKey):
    if (priorityKey == IssuePriority.High):
        priorityName = u'高'
    if (priorityKey == IssuePriority.Middle):
        priorityName = u'中'
    if (priorityKey == IssuePriority.Low):
        priorityName = u'低'
    return priorityName


def getPriorityKeyByName(priorityName):
    if (priorityName == u'高'):
        priorityKey = IssuePriority.High
    if (priorityName == u'中'):
        priorityKey = IssuePriority.Middle
    if (priorityName == u'低'):
        priorityKey = IssuePriority.Low
    return priorityKey


def getStatusNameByKey(statusKey):
    if (statusKey == IssueStatus.Open):
        statusName = u'新建'
    if (statusKey == IssueStatus.Fixed):
        statusName = u'已修复'
    if (statusKey == IssueStatus.Closed):
        statusName = u'已关闭'
    if (statusKey == IssueStatus.Canceled):
        statusName = u'取消'
    return statusName


def getStatusKeyByName(statusName):
    if (statusName == u'新建'):
        statusKey = IssueStatus.Open
    if (statusName == u'已修复'):
        statusKey = IssueStatus.Fixed
    if (statusName == u'已关闭'):
        statusKey = IssueStatus.Closed
    if (statusName == u'取消'):
        statusKey = IssueStatus.Canceled
    return statusKey


def getCategoryKeyByName(categoryName):
    if (categoryName == 'Bug'):
        categoryKey = 1
    if (categoryName == 'Issue'):
        categoryKey = 2
    return categoryKey


def ImportToDB(projectid, filepath):
    ext = filepath.split('.')[-1]
    if ext not in ['xls', 'xlsx']:
        return False
    data = xlrd.open_workbook(filepath)
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    record = {}
    recordlist = []
    if nrows > 1 and ncols >= 1:
        for rnum in range(1, nrows):
            row = table.row_values(rnum)
            if row:
                record = {}
                for cnum in range(ncols):
                    record['%d' % cnum] = str(row[cnum])
                recordlist.append(record)

    project_id = category_id = priority = assign_to = creator = 0
    subject = description = ''
    try:
        for r in recordlist:
            project_id = int(projectid)
            category_id = int(getCategoryKeyByName(r['2']))
            subject = r['3']
            description = r['4']
            priority = int(getPriorityKeyByName(r['5']))
            assign_to = int(userprofile.get_userid_by_name(r['7']))
            creator = int(userprofile.get_userid_by_name(r['7']))
            create(project_id, category_id, subject, priority, assign_to, description, creator)
    except Exception, e:
        print 'error message:', e.message
        return False
    return True
