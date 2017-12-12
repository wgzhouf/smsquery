#!/bin/python3
# coding=utf-8


import os
import cgi
from smsquery.util import user, ecpsms
from smsquery.log import ecplog

form = cgi.FieldStorage()
print("Content-type:text/json;charset=utf-8\n")

visiter_IP = os.environ['REMOTE_ADDR']
visiter_KEY = form["key"].value
CODE = "480"
visiter_NAME = "NULL"
info_message = ""
token = ""

if user.isVIP(visiter_IP):
    CODE, visiter_NAME = user.checkTheVIP(visiter_IP, visiter_KEY)
    if CODE == "200":
        info_message = "用户：" + visiter_NAME + " IP：" + visiter_IP + " 正在使用系统..."
        token = ecpsms.md5((visiter_NAME + visiter_IP + visiter_KEY).encode('utf-8'))

    else:
        info_message = "IP：" + visiter_IP + " 的KEY输入错误，已阻止登录..."
else:
    info_message = "IP：" + visiter_IP + " 不是登记在册的IP，已拦截..."


response = "{\"code\":\"" + CODE + "\", \"name\":\"" + visiter_NAME + "\", \"token\":\"" + token + "\"}"
print(response)

querysmscontents_loger = ecplog.getSMSQueryLoger('..')
querysmscontents_loger.info(info_message)

