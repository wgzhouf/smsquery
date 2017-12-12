#!/bin/python3
# coding=utf-8

import cgi
import os
from smsquery.util import user, ecpsms
from smsquery.log import ecplog

form = cgi.FieldStorage()
visiter_IP = os.environ['REMOTE_ADDR']
visiter_Name = user.getNAMEuseIP(visiter_IP)

# ==================打印包头=======================
print("Content-type:text/json;charset=utf-8\n")


# ==================返回JSON=======================
ecpsms.path = ".."  # the basic root is the webroot
account = form["account"].value
accountnumber = form["accountnumber"].value
versiontype = '117'
date = ecpsms.getECPdate()
starttime = form["starttime"].value
endtime = form["endtime"].value
startindex = form["startindex"].value
endindex = form["endindex"].value
token = form["token"].value

accountgen = ecpsms.genAccount(account, date)
ticketgen = ecpsms.genTicket(account, date)

if user.isTokenCorrect(visiter_IP, token):
    requestdata = ecpsms.gensmsContentxml(accountgen, ticketgen, accountnumber, starttime, endtime, versiontype, startindex, endindex)
    xmlresult = ecpsms.postxmltoserver('http://115.239.133.243/zjEcpServItf2.67/Main', requestdata)
    totalnumber, jsonresult = ecpsms.transSMSContantXMLtoJSON(xmlresult)
    info_message = "用户：" + visiter_Name + " IP：" + visiter_IP + " 正在查询 账号" + account + \
                   " " + starttime + " 至 " + endtime + \
                   " 第 " + startindex + " 条至第 " + endindex + " 条的数据"
else:
    jsonresult = "{\"code\":\"500\"}"
    info_message = " IP：" + visiter_IP + " 正在非法调用，已拦截"
print(jsonresult)


# ==================打印日志=======================
querysmscontents_loger = ecplog.getSMSQueryLoger('..')
querysmscontents_loger.info(info_message)

