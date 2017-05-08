# -*-coding:utf-8 -*-
import requests
import re
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')


def Get(Url, headers):
    s = requests.Session()
    if headers:
        s.headers.update(headers)
    else:
        s.headers.update(
            {
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
                'Connection': 'Keep-Alive', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept-Encoding': 'gzip, deflate'})

    try:
        if Url.find('https') == 0 and Url.index('https') == 0:
            r = s.get('%s' % Url, verify=False)
        else:
            r = s.get('%s' % Url)

        if r.encoding.lower() != 'utf-8':
            r.encoding = 'gbk'
        return r.status_code, r.content
    except Exception, e:
        return -1, e.message


def Post(Url, data, headers):
    s = requests.Session()
    if headers:
        s.headers.update(headers)
    else:
        s.headers.update(
            {
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
                'Connection': 'Keep-Alive', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept-Encoding': 'gzip, deflate'})
    try:
        if Url.find('https') == 0 and Url.index('https') == 0:
            r = s.post("%s" % Url, data=data, verify=False)
        else:
            r = s.post("%s" % Url, data=data)

        if r.encoding.lower() != 'utf-8':
            r.encoding = 'gbk'
        return r.status_code, r.content
    except Exception, e:
        return -1, e.message


def Get_S(session, url, headers):
    s = requests.Session()
    if headers:
        s.headers.update(headers)
    else:
        s.headers.update(
            {
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
                'Connection': 'Keep-Alive', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept-Encoding': 'gzip, deflate'})

    try:
        if url.find('https') == 0 and url.index('https') == 0:
            r = s.get('%s' % url, verify=False)
        else:
            r = s.get('%s' % url)

        if r.encoding.lower() != 'utf-8':
            r.encoding = 'gbk'
        return r.status_code, r.content
    except Exception, e:
        return -1, e.message


def Post_S(session, url, data, headers):
    s = session
    if headers:
        s.headers.update(headers)
    else:
        s.headers.update(
            {
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
                'Connection': 'Keep-Alive', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept-Encoding': 'gzip, deflate'})
    try:
        if url.find('https') == 0 and url.index('https') == 0:
            r = s.post("%s" % url, data=data, verify=False)
        else:
            r = s.post("%s" % url, data=data)

        if r.encoding.lower() != 'utf-8':
            r.encoding = 'gbk'
        return r.status_code, r.content
    except Exception, e:
        return -1, e.message

"""
if __name__ == '__main__':
    Url = 'http://172.16.212.243:10000/crm_business/login'
    # Url = 'http://172.16.212.243:10000/crm_business/main/queryCertType'
    # Url = 'https://sso.teamshub.com/login?service=http%3A%2F%2Feip.si-tech.com.cn%2F'
    PostData = {'routeCode': '0'}
    code, ret = Post(Url, PostData)
    # ret = Get(Url)
    print code, ret
"""
