#!/bin/python3
# coding=utf-8
import cgi
import os

from smsquery.util import user, ecpsms

form = cgi.FieldStorage()
visiter_IP = os.environ['REMOTE_ADDR']

print("Content-type:text/json;charset=utf-8\n")

ecpsms.path = ".."  # the basic root is the webroot
account = form["account"].value
accountnumber = form["accountnumber"].value
versiontype = '117'
date = ecpsms.getECPdate()
starttime = form["starttime"].value
smsid = form["smsid"].value
token = form["token"].value

accountgen = ecpsms.genAccount(account, date)
ticketgen = ecpsms.genTicket(account, date)

if user.isTokenCorrect(visiter_IP, token):
    requestdata = ecpsms.gensmsDetailInfoGetxml(accountgen, ticketgen, accountnumber, starttime, versiontype, smsid)
    xmlresult = ecpsms.postxmltoserver('http://115.239.133.243/zjEcpServItf2.67/Main', requestdata)
    totalnumber, jsonresult = ecpsms.transSMSDetailXMLtoJSON(xmlresult)
else:
    jsonresult = "{\"code\":\"500\"}"
print(jsonresult)
