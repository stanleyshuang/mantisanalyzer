#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Auther:   Stanley Huang
# Project:  mantisanalyzer 1.0
# Date:     2021-06-03
#
import os
import sys

from mantisconnect.simple_project import Issue
from mantisconnect.simple_project import SimpleProject
from mantisconnect.connector_interface import create_mantis_soap_connector
from util.util_text_file import get_lines

def output_text(filepath, content):
    fp = open(filepath, "a")    # 開啟檔案
    fp.write(content)           # 寫入 This is a testing! 到檔案
    fp.close()                  # 關閉檔案

### get argv[1] as input
if len(sys.argv) >=2:
    issue_id = sys.argv[1]
else:
    print('usage: python main.py [issue id]\n')
    quit()

### the main program
# Get environment variables
mantis_url = os.environ.get('mantis_url')
username = os.environ.get('mantis_username')
password = os.environ.get('mantis_password')
mantis_project = os.environ.get('mantis_project')

### read file in all_lines
mc = create_mantis_soap_connector(mantis_url)
mc.set_user_passwd(username, password)
mc.connect()

p = SimpleProject(mc, mantis_project)
filter_name = "all security issues"
issue_list = p.request_filter_all_issues(filter_name)
for issue in issue_list:
    print("{0} {1}".format(issue.issue_id, issue.summary))