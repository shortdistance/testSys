# -*- coding: utf-8 -*-

from scripts.models import Task, TaskStatus, UserProfile, database
from datetime import datetime
from sqlalchemy.orm import joinedload
from scripts.config import *
from scripts.models.project import Project
from sqlalchemy import func
from scripts.services import userprofile, mail


def create(task_id, project_id, task_name, task_type, priority, assign_to, description, tasklinkcase, creator):
    session = database.get_session()
    task_name = task_name.strip()
    t = Task()
    t.TaskId = task_id
    t.ProjectId = project_id
    t.TaskName = task_name
    t.TaskType = task_type
    t.Priority = priority
    t.Progress = 0
    if assign_to == -1:
        t.AssignTo = creator
    else:
        t.AssignTo = assign_to
    assign_to = t.AssignTo
    t.Effort = 0
    t.Status = TaskStatus.New
    t.Description = description
    t.TaskLinkCase = tasklinkcase
    t.Creator = creator
    t.CreateDate = datetime.now()
    t.LastUpdateDate = datetime.now()

    session.add(t)
    session.commit()
    session.close()

    calcprogress(project_id)

    if ENABLE_MAIL_NOTICE:
        u = userprofile.get_user_by_id(assign_to)
        body = mail.render_mail_template('Task/NoticeAssignTo.html', TaskName=task_name,
                                         Description=description, SystemUrl=HOST)
        mail.send_mail(u.Email, u'指派给您的新任务 ' + task_name, body)


def query(projectid, task_name, task_type, assign_to, status_new, status_in_progress, status_completed, status_canceled,
          order_by, page_no):
    session = database.get_session()

    filters = []
    status = []
    projectid = int(projectid)
    task_name = task_name.strip()

    if task_type > 0:
        filters.append(Task.TaskType == task_type)
    if projectid > 0:
        filters.append(Task.ProjectId == projectid)
    if len(task_name) > 0:
        filters.append(Task.TaskName.like('%' + task_name + '%'))
    if not assign_to == 0:
        filters.append(Task.AssignTo == assign_to)
    if status_new:
        status.append(TaskStatus.New)
    if status_in_progress:
        status.append(TaskStatus.InProgress)
    if status_completed:
        status.append(TaskStatus.Completed)
    if status_canceled:
        status.append(TaskStatus.Canceled)
    if len(status) > 0:
        filters.append(Task.Status.in_(status))

    q = session.query(Task).join(UserProfile, UserProfile.UserId == Task.Creator).join(UserProfile,
                                                                                       UserProfile.UserId == Task.AssignTo)
    for f in filters:
        q = q.filter(f)
    (row_count, page_count, page_no, page_size, data) = database.pager(q, order_by, page_no, PAGESIZE)

    session.close()
    return (row_count, page_count, page_no, page_size, data)


def get(task_id):
    session = database.get_session()
    task = session.query(Task).options(joinedload(Task.CreatorProfile), joinedload(Task.AssignToProfile)).filter(
        Task.TaskId == task_id).one()
    session.close()
    return task


def update(task_id, task_name, task_type, assign_to, priority, progress, status, effort, description, tasklinkcase):
    session = database.get_session()

    task_name = task_name.strip()
    task = session.query(Task).filter(Task.TaskId == task_id).one()
    changeAssignTo = not (task.AssignTo == assign_to)

    task.TaskName = task_name
    task.TaskType = task_type
    task.AssignTo = assign_to
    task.Priority = priority
    task.Progress = progress
    task.Status = status
    task.Description = description
    task.TaskLinkCase = tasklinkcase
    task.Effort = float(effort)
    task.LastUpdateDate = datetime.now()
    project_id = task.ProjectId
    session.commit()
    session.close()

    calcprogress(project_id)

    if ENABLE_MAIL_NOTICE and changeAssignTo:
        u = userprofile.get_user_by_id(assign_to)
        body = mail.render_mail_template('Task/NoticeAssignTo.html', TaskName=task_name,
                                         Description=description, SystemUrl=HOST)
        mail.send_mail(u.Email, u'指派给您的新任务 ' + task_name, body)

    return True


def calcprogress(project_id):
    session = database.get_session()

    all_project_task = session.query(Task).filter(Task.ProjectId == project_id).count()
    complete_project_task = session.query(Task).filter(Task.ProjectId == project_id).filter(
        Task.Status.in_([TaskStatus.Completed, TaskStatus.Canceled])).count()

    if all_project_task == 0:
        session.query(Project).filter(Project.ProjectId == project_id).update(
            {'Progress': (0 * 100.0), 'LastUpdateDate': datetime.now()})
    else:
        session.query(Project).filter(Project.ProjectId == project_id).update(
            {'Progress': (complete_project_task * 100.0 / all_project_task), 'LastUpdateDate': datetime.now()})
    session.commit()
    session.close()


def delete(task_id):
    session = database.get_session()

    task = session.query(Task).filter(Task.TaskId == task_id).one()
    project_id = task.ProjectId
    session.delete(task)
    session.commit()
    session.close()

    calcprogress(project_id)


def statistics(project_id):
    session = database.get_session()

    task_status = session.query(Task.Status, func.count(Task.Status)).filter(Task.ProjectId == project_id).group_by(
        Task.Status).all()
    task_priority = session.query(Task.Priority, func.count(Task.Priority)).filter(
        Task.ProjectId == project_id).group_by(Task.Priority).all()

    session.commit()
    session.close()

    return (task_status, task_priority)
