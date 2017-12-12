#!/bin/python3
# coding=utf-8
import time
import os
from urllib import request
from xml.dom.minidom import parseString
import xml.dom.minidom

path = "."

def gensmsContentxml(accountGen='', ticketGen='', businessNumber='', startTime='', endTime='', versionType='', startindex='', endindex=''):
    """
    组装查询短信内容用的XML
    :param accountGen: 加密账号
    :param ticktGen: 加密token
    :param businessNumber: 业务号码
    :param startTime: 开始时间
    :param endTime:结束时间
    :param versionType: 版本号
    :return: 
    """
    smsContentxml = ''

    try:
        with open(os.path.join(path, 'smscontentxml'), 'r', encoding='utf-8') as fileobj:
            lines = fileobj.readlines()
    except FileNotFoundError:
        return 0

    for line in lines:
        smsContentxml += line
    smsContentxml = smsContentxml.replace('Account=\"account\"', 'Account=\"' + accountGen + '\"')
    smsContentxml = smsContentxml.replace('Ticket=\"ticket\"', 'Ticket=\"' + ticketGen + '\"')
    smsContentxml = smsContentxml.replace('<AccountPhone>accountphone<', '<AccountPhone>' + businessNumber + '<')
    smsContentxml = smsContentxml.replace('VersionType=\"versiontype\"', 'VersionType=\"' + versionType + '\"')
    smsContentxml = smsContentxml.replace('<StartTime>startime ', '<StartTime>' + startTime + ' ')
    smsContentxml = smsContentxml.replace('<EndTime>endtime ', '<EndTime>' + endTime + ' ')
    smsContentxml = smsContentxml.replace('<StartIndex>startindex', '<StartIndex>' + startindex)
    smsContentxml = smsContentxml.replace('<EndIndex>endindex', '<EndIndex>' + endindex)

    return smsContentxml


def gensmsDetailInfoGetxml(accountGen='', ticketGen='', businessNumber='', startTime='' , versionType='', smsid=''):

    smsDetailInfoGetxml = ''

    try:
        with open(os.path.join(path, 'smsDetailInfoGetxml'), 'r', encoding='utf-8') as fileobj:
            lines = fileobj.readlines()
    except FileNotFoundError:
        return 0

    for line in lines:
        smsDetailInfoGetxml += line

    smsDetailInfoGetxml = smsDetailInfoGetxml.replace('Account=\"account\"', 'Account=\"' + accountGen + '\"')
    smsDetailInfoGetxml = smsDetailInfoGetxml.replace('Ticket=\"ticket\"', 'Ticket=\"' + ticketGen + '\"')
    smsDetailInfoGetxml = smsDetailInfoGetxml.replace('<AccountPhone>accountphone<', '<AccountPhone>' + businessNumber + '<')
    smsDetailInfoGetxml = smsDetailInfoGetxml.replace('<StartTime>starttime ', '<StartTime>' + startTime + ' ')
    smsDetailInfoGetxml = smsDetailInfoGetxml.replace('VersionType=\"versiontype\"', 'VersionType=\"' + versionType + '\"')
    smsDetailInfoGetxml = smsDetailInfoGetxml.replace('<SMSID>smsid', '<SMSID>' + smsid)

    return smsDetailInfoGetxml

def md5(input):
    import hashlib
    my_md5 = hashlib.md5()
    my_md5.update(input)
    return my_md5.hexdigest()


def getECPdate():
    current_time = time.strftime("%Y%m%d%H%M%S")
    return current_time


def encode(account=''):
    hexString = '0123456789ABCDEF'
    mybyts = bytearray(account, 'utf-8')
    sb = ""
    for mybyte in mybyts:
       sb += hexString[(mybyte & 0xF0) >> 4]
       sb += hexString[(mybyte & 0xF) >> 0]
    return sb


def genAccount(account='', ECPdate=''):
    accountHex = encode(account)
    timePart1 = ECPdate[0:5]
    timePart2 = ECPdate[5:]
    return timePart1 + accountHex + timePart2


def genTicket(account='', ECPdate=''):
    return md5((ECPdate[0:5] + account + ECPdate[5:]).encode('utf-8'))


def postxmltoserver(url='', data=''):
    headers = {
        'Content-Type': 'text/xml',
        'User-Agent': 'Jakarta Commons-HttpClient/3.1'
    }
    req = request.Request(url, data.encode('utf-8'), headers)
    res = request.urlopen(req)
    result = res.read().decode('utf-8')
    res.close()

    return result


def transSMSContantXMLtoJSON(xmlcontaint=''):
    DOMTree = xml.dom.minidom.parseString(xmlcontaint)
    collection = DOMTree.documentElement
    totalnumber = collection.getElementsByTagName("TotalNumber")[0].childNodes[0].data
    result_json = "{"
    result_json += "\"code\":\"200\","
    result_json += "\"totalnumber\":" + totalnumber + ","
    result_json += "\"smslists\":["
    SMSInfos = collection.getElementsByTagName("SMSInfo")
    count = 0

    for smsinfo_node in SMSInfos:
        count += 1
        result_json += "{"
        smsid = smsinfo_node.getElementsByTagName("SMSID")[0].childNodes[0].data
        phonenamber = smsinfo_node.getElementsByTagName("PhoneNumber")[0].childNodes[0].data
        content = smsinfo_node.getElementsByTagName("Content")[0].childNodes[0].data
        sendtime = smsinfo_node.getElementsByTagName("SendTime")[0].childNodes[0].data
        smstotal = smsinfo_node.getElementsByTagName("SMSTotal")[0].childNodes[0].data
        sucsmstotal = smsinfo_node.getElementsByTagName("SucSMSTotal")[0].childNodes[0].data
        result_json += "\"smsid\":\"" + smsid + "\","
        result_json += "\"phonenamber\":\"" + phonenamber + "\","
        result_json += "\"content\":\"" + content + "\","
        result_json += "\"sendtime\":\"" + sendtime + "\","
        result_json += "\"sucsmstotal\":" + sucsmstotal + ","
        result_json += "\"smstotal\":" + smstotal + "}"
        if count < len(SMSInfos):
            result_json += ","
    result_json += "]}"
    result_json = result_json.replace("\n", "")
    return totalnumber, result_json


def transSMSDetailXMLtoJSON(xmlcontaint=''):
    DOMTree = xml.dom.minidom.parseString(xmlcontaint)
    collection = DOMTree.documentElement
    totalnumber = collection.getElementsByTagName("TotalNumber")[0].childNodes[0].data
    SMSDetailInfos = collection.getElementsByTagName("SMSDetailInfo")
    count = 0

    result_json = "{"
    result_json += "\"code\":\"200\","
    result_json += "\"totalnumber\":" + totalnumber + ","
    result_json += "\"smsdetaillists\":["

    for smsdetailinfo in SMSDetailInfos:
        count += 1
        result_json += "{"

        phonenumber = smsdetailinfo.getElementsByTagName("PhoneNumber")[0].childNodes[0].data
        # succeessnum = smsdetailinfo.getElementsByTagName("SucceessNum")[0].childNodes[0].data
        # totalnum = smsdetailinfo.getElementsByTagName("TotalNum")[0].childNodes[0].data
        errorcode = smsdetailinfo.getElementsByTagName("ErrorCode")[0].childNodes[0].data

        result_json += "\"phonenumber\":\"" + phonenumber + "\","
        # result_json += "\"succeessnum\":\"" + succeessnum + "\","
        # result_json += "\"totalnum\":\"" + totalnum + "\","
        result_json += "\"errorcode\":\"" + errorcode + "\"}"
        if count < len(SMSDetailInfos):
            result_json += ","

    result_json += "]}"
    result_json = result_json.replace("\n", "")

    return totalnumber, result_json