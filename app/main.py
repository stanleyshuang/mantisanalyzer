#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Auther:   StanleyS Huang
# Project:  mantisanalyzer 1.0
# Date:     2021-10-03
#
import os, sys

from datetime import datetime
from jira import JIRA

from pkg.global_conf import var
from pkg._mantis.mantis import mantis, qpkg_install_time
from pkg._mantis.diagnostics import qts_install_time, qpkg_conf_update_info, open_conf, linefilter
from pkg._mantis.summary import summarize_qpkg_install_time, summarize_qts_install_time, summarize_raid_metadata
from pkg._gsheet.gsheet_incident_summary import gsheet_incident_summary
from pkg._gsheet.gsheet_vulnrep import gsheet_vulnrep
from pkg._util import util_globalvar
from pkg._util.util_file import create_folder

def output_text(filepath, content):
    fp = open(filepath, "a")    # 開啟檔案
    fp.write(content)           # 寫入 This is a testing! 到檔案
    fp.close()                  # 關閉檔案

def get_jira_issue(server, username, password, jira_id):
    jira = JIRA(basic_auth=(username, password), options={'server': server})
    return jira, jira.issue(jira_id, expand='changelog')

def get_mantis_ticket(mantis_url, username, password, project, mantis_id, downloads):
    return mantis(mantis_url, username, password, project, mantis_id, downloads)

def usage():
    print('USAGE:        python main.py [mode] [summarize:mantis_list|parse:mantis_id|mantis_id]')
    print('--')
    print('mode:         one of --regular or --verbose, default value is --regular')
    print('mantis_list:  text file that records MantisBT ID list')
    print('mantis_id:    MantisBT ID for example, #83228')
    print('-------------------------------------------------')
    print('USAGE:    python main.py cmd')
    print('--')
    print('cmd:      one of --batch or --test')
    print('          --batch for batch running')
    print('          --test for unit test')
    quit()
  
### the main program
if len(sys.argv)==1:
    usage()

now = datetime.now()
str_now = now.strftime("%Y-%m-%d")

### get argv[1] as input
jira_id = ''
cmd = 'standard'
mode = 'regular'
mantis_list = 'global'
mantis_id = ''
str_incident_date = str_now
for idx in range(1, len(sys.argv)):
    if sys.argv[idx] in ['--test', '--batch']:
        cmd = sys.argv[idx][2:]
    elif sys.argv[idx] in ['test', 'batch']:
        cmd = sys.argv[idx]
    elif sys.argv[idx] in ['--verbose']:
        mode = sys.argv[idx][2:]
    elif sys.argv[idx] in ['verbose']:
        mode = sys.argv[idx]
    elif sys.argv[idx].find('summarize:')>=0:
        cmd = 'summarize'
        mantis_list = sys.argv[idx][10:]
    elif sys.argv[idx].find('linefilter:')>=0:
        cmd = 'linefilter'
        mantis_id = int(sys.argv[idx][11:].replace("#", ""))
    elif sys.argv[idx].find('parse:')>=0:
        cmd = 'parse'
        mantis_id = int(sys.argv[idx][6:].replace("#", ""))
    elif sys.argv[idx].find('date:')>=0:
        str_incident_date = sys.argv[idx][5:]
    elif sys.argv[idx].find('unittest')>=0:
        cmd = 'unittest'
    else:
        cmd = 'parse'
        mantis_id = int(sys.argv[idx].replace("#", ""))

# Get environment variables
jira_url = os.environ.get('jira_url')
jira_username = os.environ.get('jira_username')
jira_password = os.environ.get('jira_password')

google_sheet_key = os.environ.get('google_sheet_key')
google_api_credential = os.environ.get('google_api_credential')

mantis_url = os.environ.get('mantis_url')
username = os.environ.get('mantis_username')
password = os.environ.get('mantis_password')
mantis_project = os.environ.get('mantis_project')

### Create data folder
apphome = os.environ.get('apphome')
data = apphome + '/data'
create_folder(data)

### Create downloads folder
downloads = apphome + '/downloads'
create_folder(downloads)

gsheet = gsheet_incident_summary(the_credential=google_api_credential, the_key=google_sheet_key, url=os.environ.get('jira_url'))
gsheet_v = gsheet_vulnrep(the_credential=google_api_credential, the_key=google_sheet_key, url=os.environ.get('jira_url'))

if cmd=='batch':
    pass
elif cmd=='test':
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
elif cmd=='linefilter':
    diagnostics_path = downloads+'/'+str(mantis_id)
    if mantis_id in util_globalvar.get_value('g_dont_parse_mantis_id_list') and os.path.isdir(diagnostics_path):
        linefilter(mantis_id, diagnostics_path, gsheet_v)
elif cmd=='summarize':
    summarize_qts_install_time(mantis_url, username, password, mantis_project, data+'/'+mantis_list+'.csv', downloads, str_incident_date, gsheet, mantis_list)
    summarize_raid_metadata(mantis_url, username, password, mantis_project, data+'/'+mantis_list+'.csv', downloads, str_incident_date, gsheet, mantis_list)
    summarize_qpkg_install_time(mantis_url, username, password, mantis_project, data+'/'+mantis_list+'.csv', downloads, str_incident_date, gsheet, mantis_list)
elif cmd=='unittest':
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)
else: # cmd in ['standard', 'parse']
    qpkg_name_2_versions = {}
    diagnostics_path = downloads+'/'+str(mantis_id)
    if mantis_id in util_globalvar.get_value('g_dont_parse_mantis_id_list') and os.path.isdir(diagnostics_path):
        the_qts_install_time = qts_install_time(mantis_id, diagnostics_path, str_incident_date)
        the_qpkg_conf_update_info = qpkg_conf_update_info(diagnostics_path)
        qpkg_install_time(mantis_id, diagnostics_path, str_incident_date, qpkg_name_2_versions, the_qpkg_conf_update_info, gsheet_v)
    else:
        mantis = get_mantis_ticket(mantis_url, username, password, mantis_project, mantis_id, downloads)
        # mantis.enum_issue_fields()
        the_qts_install_time = mantis.qts_install_time(str_incident_date)
        the_qpkg_conf_update_info = mantis.qpkg_conf_update_info()
        mantis.qpkg_install_time(str_incident_date, qpkg_name_2_versions, the_qpkg_conf_update_info, gsheet_v)
    print('### Summarize {mantis_id} data'.format(mantis_id=str(mantis_id)))

    if the_qts_install_time and 'Model' in the_qts_install_time:
        models = set([the_qts_install_time['Model']])
        print('   -- Models')
        for model in models:
            print('      - ' + model)
                
    if the_qts_install_time and 'Firmware' in the_qts_install_time:
        firmwares = set([the_qts_install_time['Firmware']])
        print('   -- Firmware')
        for firmware in firmwares:
            print('      - ' + firmware)

    if mantis_id in util_globalvar.get_value('g_dont_parse_mantis_id_list') and os.path.isdir(diagnostics_path):
        the_qpkg_conf = open_conf(diagnostics_path, conf_path='/etc/config/qpkg.conf')
        if the_qpkg_conf:
            sections = the_qpkg_conf.sections()
        else:
            quit()
    else:
        sections = mantis.qpkg_sections()       
    if sections:
        qpkgs = set(sections)
        print('### Summarize {mantis_id} data'.format(mantis_id=str(mantis_id)))
        print('   -- QPKGs')
        for qpkg_name in qpkgs:
            print('      - ' + qpkg_name)
            if qpkg_name in qpkg_name_2_versions:
                for item in qpkg_name_2_versions[qpkg_name]:
                    print('        - ' + item)

    if mantis and mode=='verbose':
        pass
