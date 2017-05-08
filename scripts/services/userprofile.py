# -*- coding: utf-8 -*-

from scripts.models import UserProfile, UserStatus, database
from datetime import datetime
from scripts.config import PAGESIZE
from sqlalchemy.sql.expression import or_
from scripts.config import *


def get(email):
    session = database.get_session()
    user = session.query(UserProfile).filter(UserProfile.Email == email).first()
    session.close()
    return user


def get_user_by_id(user_id):
    session = database.get_session()
    user = session.query(UserProfile).filter(UserProfile.UserId == user_id).one()
    session.close()
    return user


def get_userid_by_name(username):
    session = database.get_session()
    user = session.query(UserProfile).filter(UserProfile.Nick == username).one()
    session.close()
    if user:
        return user.UserId
    else:
        return 1


def change_password(raw_password, new_password, user_id):
    session = database.get_session()
    user = session.query(UserProfile).filter(UserProfile.UserId == user_id).first()
    if not user.Password == raw_password:
        session.close()
        return False
    user.Password = new_password
    session.commit()
    session.close()
    return True


def udpate_profile(email, nick, user_id):
    email = email.strip()
    nick = nick.strip()
    session = database.get_session()
    user = session.query(UserProfile).filter(UserProfile.UserId == user_id).first()
    if not user.Email == email:
        exist = session.query(UserProfile).filter(UserProfile.Email == email).count() > 0
        if exist:
            session.close()
            return False
        else:
            user.Email = email
    user.Nick = nick
    session.commit()
    session.close()
    return True


def register(email, nick, password):
    email = email.strip()
    nick = nick.strip()
    session = database.get_session()
    exist = session.query(UserProfile).filter(UserProfile.Email == email).count() > 0
    userid = -1
    if not exist:
        user = UserProfile()
        user.Email = email
        user.Nick = nick
        user.Password = password
        user.EmailVerify = False
        user.Status = UserStatus.Enabled
        user.IsAdmin = False
        user.RegDate = datetime.now()
        session.add(user)
        session.commit()
        userid = user.UserId
    session.close()
    return (exist, userid)


def query_user(mail_or_nick, status, order_by, page_no):
    session = database.get_session()
    filters = []
    if len(mail_or_nick) > 0:
        filters.append(
            or_(UserProfile.Email.like('%' + mail_or_nick + '%'), UserProfile.Nick.like('%' + mail_or_nick + '%')))
    if not status == -1:
        filters.append(UserProfile.Status == status)
    q = session.query(UserProfile)
    for f in filters:
        q = q.filter(f)
    (row_count, page_count, page_no, page_size, data) = database.pager(q, order_by, page_no, PAGESIZE)
    session.close()
    return (row_count, page_count, page_no, page_size, data)


def enable_user(user_id):
    session = database.get_session()
    user = session.query(UserProfile).filter(UserProfile.UserId == user_id).update({'Status': UserStatus.Enabled})
    session.commit()
    session.close()


def disable_user(user_id):
    session = database.get_session()
    user = session.query(UserProfile).filter(UserProfile.UserId == user_id).update({'Status': UserStatus.Disabled})
    session.commit()
    session.close()


def reset_password(user_id):
    session = database.get_session()
    user = session.query(UserProfile).filter(UserProfile.UserId == user_id).update({'Password': '123456'})
    session.commit()
    session.close()


def assign_admin(user_id):
    session = database.get_session()
    user = session.query(UserProfile).filter(UserProfile.UserId == user_id).one()
    user.IsAdmin = not user.IsAdmin
    session.commit()
    session.close()
