#!/usr/bin/python
# -*- coding:utf-8 -*-

import httplib
import httplib2
import urllib
import json


def http_post(host, port, url, params, timeout=60):
    httpClient = None
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:17.0) Gecko/20100101 Firefox/17.0',
         'Connection': 'Keep-Alive', 'Content-Type': 'text/html; charset=utf-8'}
        httpClient = httplib.HTTPConnection(host, int(port), timeout)
        httpClient.request('POST', url, params, headers)
        response = httpClient.getresponse()
        code = response.status
        msg = response.read().decode('utf-8')

    except Exception, e:
        code = -1
        msg = e.message

    finally:
        if httpClient:
            httpClient.close()
        return code, msg


def http_get(host, port, url, timeout=60):

    httpClient = None
    code = -1
    msg = ''
    try:
        httpClient = httplib.HTTPConnection(str(host), int(port), timeout)
        httpClient.request('GET', url)
        response = httpClient.getresponse()
        code = response.status
        msg = response.read()

    except Exception, e:
        code = -1
        msg = e.message
        print msg

    finally:
        if httpClient:
            httpClient.close()
        return code, msg


def analyseUrl(url):
    '''
    eg:
    url = 'http://172.21.1.30:51900/esbWS/rest/SHPOCRouteTest'
    host, port, suburl = analyseUrl(url)
    '''
    host = ''
    port = ''
    sub_url = ''
    host_port = url.split('://')[1].split('/')[0]
    if len(host_port.split(':')) == 2:
        host = host_port.split(':')[0]
        port = host_port.split(':')[1]
    else:
        host = host_port.split(':')[0]
        port = '80'

    sub_url_list = []
    sub_url_list = url.split('://')[1].split('/')[1:]
    sub_url = '/' + '/'.join(sub_url_list)

    return host, port, sub_url


if __name__ == '__main__':

    url = 'http://172.16.212.243:10000/crm_business/login'
    host, port, suburl = analyseUrl(url)

    params = '{"routeCode": 0}'
    statusCode, responseMsg = http_post(host, port, suburl, params, timeout=160)
    print statusCode
    print responseMsg.decode("GBK")
