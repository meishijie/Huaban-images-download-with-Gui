#!/usr/bin/env python
# -*- encoding:utf-8 -*-


import os
import re
import sys
import time
import urllib
import urllib.request
from tkinter.filedialog import askdirectory
import tkinter as tk
from tkinter import *
from tkinter import ttk

# reload(sys)

global iid
iid = '点击后等待下载'
global GPATH
GPATH = ''


maxid = ''
txtid = ''
firstid = ''
nowid = ''
limit = 100
# 他默认允许的limit为100
# changelabel(pid+'下载中')
url = 'http://login.meiwu.co/boards/36429482' + \
    '/?max=' + maxid + '&limit=' + str(limit) + '&wfl=1'
i_headers = {
    "User-Agent": "Mozilla/5.0 (WINdows NT 6.1; rv:2.0.1)Gecko/20100101 Firefox/4.0.1",
    "Connection": "keep-alive",
    "Host": "login.meiwu.co",
    "Accept": "application/json"
}
req = urllib.request.Request(url, headers=i_headers)
html = urllib.request.urlopen(req).read().decode('utf-8')
print(html)
# reg = re.compile('"pin_id":(.*?),.+?"file":{"farm":"farm1", "bucket":"hbimg",.+?"key":"(.*?)",.+?"type":"image/(.*?)"', re.S)
reg = re.compile(
    '"pin_id":(.*?),.+?"file":\{"id":.+?"key":(.*?),.+?"type":"image\/(.*?)"', re.S)
groups = re.findall(reg, html)
firstid = groups[0][0]
print(groups[0][0])

# print len(text_read('beauty/'+board_id+'/1.txt'))
