# -*-coding:utf-8 -*-

def GetMidStr(content, startStr, endStr):
    content = unicode(content).replace('\'', '\\\'')
    startStr.replace('\'', '\\\'')
    endStr.replace('\'', '\\\'')
    startIndex = endIndex = 0
    if content.find(startStr) != -1:
        startIndex = content.index(startStr)
        contentnew = ''
        startIndex += len(startStr)
        contentnew = content[startIndex + 1:]
        if contentnew.find(endStr) != -1:
            endIndex = startIndex + 1 + contentnew.index(endStr)
            retmsg = u'[%s]' % content[startIndex: endIndex]
            return retmsg, content[startIndex: endIndex]
        else:
            retmsg = u'右边界[%s]不存在!!' % endStr
            return retmsg, None
    else:
        retmsg = u'左边界[%s]不存在!!' % startStr
        return retmsg, None
