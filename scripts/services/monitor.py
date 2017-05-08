# -*- coding: utf-8 -*-

from scripts.models import database
from scripts.models.monitor import HostMonitor

from scripts.config import *
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from sqlalchemy import distinct, asc, desc


def insertData(host, free_mem, idel_cpu):
    session = database.get_session();
    hm = HostMonitor()
    hm.Host = host
    hm.MemFree = free_mem
    hm.CpuIdel = idel_cpu
    hm.CreateTime = datetime.now()
    session.add(hm)
    session.commit()
    session.close()


def getData(host):
    dtnow = datetime.now()
    dt = datetime(dtnow.year, dtnow.month, dtnow.day, 0, 0, 0)
    session = database.get_session()
    q = session.query(HostMonitor).filter(HostMonitor.Host == host, HostMonitor.CreateTime > dt).order_by(
        HostMonitor.Id.desc()).limit(180).all()
    session.close()
    cpu_info = dict(name=host, data=[])
    mem_info = dict(name=host, data=[])
    temp = []
    for mon_info in q:
        temp = []
        temp.append(mon_info.CreateTime)
        temp.append(mon_info.CpuIdel)
        cpu_info['data'].append(temp)

        temp = []
        temp.append(mon_info.CreateTime)
        temp.append(mon_info.MemFree)
        mem_info['data'].append(temp)

    cpu_info['data'] = cpu_info['data'][::-1]
    mem_info['data'] = mem_info['data'][::-1]
    return cpu_info, mem_info


def getDataAll():
    session = database.get_session()
    hostlist = session.query(distinct(HostMonitor.Host)).all()
    session.close()

    cpuInfo = {}
    memInfo = {}
    retCpuInfo = []
    retMemInfo = []
    for host in hostlist:
        cpuInfo = {}
        memInfo = {}
        cpuInfo, memInfo = getData(host[0])
        retCpuInfo.append(cpuInfo)
        retMemInfo.append(memInfo)
    return retCpuInfo, retMemInfo
