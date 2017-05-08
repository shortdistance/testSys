# -*- coding: utf-8 -*-

from scripts.models.database import BaseModel
from sqlalchemy import Column, Integer, SMALLINT, String, Boolean, DateTime, Float, ForeignKey, UnicodeText
from sqlalchemy.orm import relationship
from scripts.models.userprofile import UserProfile


class IssueStatus:
    Open = 1
    Fixed = 2
    Closed = 3
    Canceled = 4


class IssueCategoryStatus:
    Enabled = 1
    Disabled = 2


class IssuePriority:
    High = 1
    Middle = 2
    Low = 3
