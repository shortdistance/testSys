# -*- coding: utf-8 -*-

import sys
from werkzeug.security import generate_password_hash
from scripts.models import database
from scripts.models.userprofile import UserProfile, UserStatus
from scripts.models.issue import IssueCategoryStatus, IssueCategory

from datetime import datetime

if '-dropcreate' in sys.argv:
    database.drop_database()
    print(u'删除数据库完成')

database.create_database()
print(u'创建数据库完成')

session = database.get_session()
admin = UserProfile()
admin.Email = 'admin@admin.com'
admin.Nick = u'admin'
admin.Password = generate_password_hash('admin')
admin.Status = UserStatus.Enabled
admin.IsAdmin = True
admin.RegDate = datetime.now()
session.add(admin)

bug = IssueCategory()
bug.CategoryName = u'Bug'
bug.Status = IssueCategoryStatus.Enabled
session.add(bug)

issue = IssueCategory()
issue.CategoryName = u'Issue'
issue.Status = IssueCategoryStatus.Enabled
session.add(issue)

session.commit()
session.close()
print(u'TestSys安装完成')
