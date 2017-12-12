#!/bin/python3
# coding=utf-8

import os
import logging
from logging.handlers import RotatingFileHandler


logname = 'smsquery.log'


def getSMSQueryLoger(relative_position='.'):
    smsquery_file_handler = RotatingFileHandler(filename=os.path.join(relative_position, logname), maxBytes=30*1024*1024, backupCount=5, encoding='utf-8')
    smsquery_formater = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    smsquery_file_handler.setFormatter(smsquery_formater)
    smsquery_loger = logging.getLogger()
    smsquery_loger.addHandler(smsquery_file_handler)
    smsquery_loger.setLevel(logging.INFO)
    return smsquery_loger