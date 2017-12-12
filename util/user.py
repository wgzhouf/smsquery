#!/bin/python3
# coding=utf-8

from smsquery.util import ecpsms

VIP_LISTS = {'10.240.80.31': {'NAME': '周峰', 'KEY': '68gk#$%3577dghvj3fg64'},
             '10.240.80.5': {'NAME': '李静子', 'KEY': 'vb34i%#$udg$@j32%8123'},
             '10.240.80.28': {'NAME': '明师傅', 'KEY': 'msf@#$%WEG#@$1234'}
}


def isVIP(IP=''):
    """
    判断是否是登记在册的IP
    :param IP:
    :return:
    """
    try:
        if VIP_LISTS[IP]:
            return True
    except:
        return False


def checkTheVIP(IP='', KEY=''):
    try:
        if VIP_LISTS[IP]['KEY'] == KEY:
            return "200", VIP_LISTS[IP]['NAME']
        else:
            return "480", "NULL"
    except:
        return "480", "NULL"

def getNAMEuseIP(IP=''):
    try:
        return VIP_LISTS[IP]['NAME']
    except:
        return "非法访问者"

def isTokenCorrect(IP='', token=''):
    result = ecpsms.md5((VIP_LISTS[IP]['NAME'] + IP + VIP_LISTS[IP]['KEY']).encode('utf-8'))
    if result == token:
        return True
    else:
        return False