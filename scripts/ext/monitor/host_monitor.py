#-*- coding:utf-8 -*-
import pysftp
import sys
import time
from testsys.testsysconfig import host_lists 
from testsys.services import service_monitor
from datetime import datetime

'''
host_list = [
	'172.16.9.144|developer|123456|22',
]
'''
class HostMonitor:
    def __init__(self, host_lists):
	if type(host_lists) == type([]):
		self.host_lists = host_lists
	else:
	    self.host_lists = None
			
    def connHosts(self):
	srv_list = [] 
	if self.host_lists:
	    for host_info in self.host_lists:
		host = host_info.split('|')[0]
		user = host_info.split('|')[1]
		passwd = host_info.split('|')[2]
		port = int(host_info.split('|')[3])
		try:
		    srv = pysftp.Connection(host=host, 
			                    username=user,
			                    password=passwd,
			                    port = port) 
		    srv_list.append(dict(srv=srv, host=host))
		except Exception,e:
		    print  'host:%s connect fail!!' % host
		    
        return 	srv_list

    def getData(self, srv_list):
	
	if  srv_list:
	    for srv in srv_list:
		idel_cpu = srv['srv'].execute('vmstat 1 2|tail -1')[0].split('\n')[0].split()[14]
		free_mem = srv['srv'].execute('free|grep "buffers/cache"')[0].split('\n')[0].split()[-1]
		service_monitor.insertData(srv['host'], int(float(free_mem)/1024), int(idel_cpu))
		
	else:
	    print 'srv list is invalid!!'
	    
    
    def disconnHosts(self, srv_list):
	if srv_list:
	    for srv in srv_list:
		srv['srv'].close()
	else:
	    print 'srv list is invalid!!'
	    

	

