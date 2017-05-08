# -*- coding: gbk -*-  

import os,sys
from datetime import *
import time


class SVNMonitor:
    def __init__(self, url, username, passwd):
        self.url = url
        self.username = username
        self.passwd = passwd
        
    def svn_log(self, startDate, endDate):
        cmd = 'svn log -r{%s}:{%s} --username %s --password %s --no-auth-cache --xml \"%s\"' % (startDate, endDate, self.username, self.passwd, self.url)
        fp = os.popen(cmd)
        ret = fp.read()
        return ret

    
'''    
if __name__ == '__main__':
    url = 'http://172.16.9.106:9001/svn/qmd'
    username = 'zhangleid'
    passwd = '1qaz2wsx'
    
    startDate = '2015-04-14'
    endDate = '2015-04-15'
    svnmon = SVNMonitor(url, username, passwd)
    ret = svnmon.svn_log(startDate, endDate)
    
    print ret.count('<logentry')
'''
        
    
    


