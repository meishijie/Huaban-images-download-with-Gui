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

board_id = '39825444'
# print board_id
if os.path.exists(GPATH + '/' + board_id) is False:
    os.mkdir(GPATH + '/' + board_id)
maxid = ''
txtid = ''
firstid = ''
nowid = ''
limit = 20
# 他默认允许的limit为100
# changelabel(pid+'下载中')
url = 'http://huaban.com/boards/' + board_id + \
    '/?max=' + maxid + '&limit=' + str(limit) + '&wfl=1'

i_headers = {
    "User-Agent": "Mozilla/5.0 (WINdows NT 6.1; rv:2.0.1)Gecko/20100101 Firefox/4.0.1",
    "Connection": "keep-alive",
    "Host": "huaban.com",
    "Accept": "application/json"
}
req = urllib.request.Request(url, headers=i_headers)
html = urllib.request.urlopen(req).read().decode("utf-8")
# reg = re.compile('"pin_id":(.*?),.+?"file":{"farm":"farm1", "bucket":"hbimg",.+?"key":"(.*?)",.+?"type":"image/(.*?)"', re.S)
# "pin_id":(.*?),.+?"file":\{"id":.+?"key":(.*?),.+?"type":"image\/(.*?)"
reg = re.compile(
    '"pin_id":(.*?),.+?"file_id":(.*?),.+?"file":\{.+?"key":(.*?),.+?"type":"image\/(.*?)"', re.S)
groups = re.findall(reg, html)
firstid = groups[0][0]
# print(groups[0][0])
print(html)

for att in groups:
    pin_id = att[0][1:-3]
    att_url = att[2][1:-1]
    img_type = att[3]
    img_url = 'http://img.hb.aicdn.com/' + att_url
    print(img_url)
    # print txtid[len(txtid) - 1]
    if len(txtid) > 0:
        if pin_id == txtid[len(txtid) - 1]:
            print('ok')
    # if urllib.request.urlretrieve(img_url, GPATH + '/' + board_id + '/' + att_url + '.' + img_type):
    #     print(img_url + ' download success!')
    # else:
    #     print(img_url + '.' + img_type + ' save failed')
