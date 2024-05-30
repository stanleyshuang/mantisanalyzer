#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Auther:   StanleyS Huang
# Project:  mantisanalyzer 1.0
# Date:     2021-12-04
#
import sys
from pkg._util import util_globalvar

util_globalvar._init()
util_globalvar.set_value('g_dont_parse_mantis_id_list', 
	[10001])