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
import socket
import threading

# reload(sys)
global allcount
allcount = 0
global groups
groups = []
global iid
iid = '点击后等待下载'
global GPATH
GPATH = ''
global downloaded

global downloadedCount
downloadedCount = 0


# if(os.path.exists('beauty') == False):
#     os.mkdir('beauty')

def text_save(content, filename, mode='a'):
    # Try to save a list variable in txt file.
    file = open(filename, mode)
    for i in range(len(content)):
        file.write(str(content[i]) + '\n')
    file.close()


def text_read(filename):
    # Try to read a txt file and return a list.Return [] if there was a
    # mistake.
    try:
        file = open(filename, 'r')
    except IOError:
        error = []
        return error
    content = file.readlines()

    for i in range(len(content)):
        content[i] = content[i][:len(content[i]) - 1]

    file.close()
    return content


def callbackfunc():
    print('ok')
    # global downloadedCount
    # downloadedCount += 1
    # print('下载了：'+str(downloadedCount))
    # global downloaded
    # downloaded.set(str(downloadedCount))


# 下载方法
def auto_down(url, filename):
    try:
        urllib.request.urlretrieve(url, filename, jindu)
    except socket.timeout:
        count = 1
        while count <= 15:
            try:
                urllib.request.urlretrieve(url, filename, jindu)
                break
            except socket.timeout:
                err_info = 'Reloading for %d time' % count if count == 1 else 'Reloading for %d times' % count
                print(err_info)
                count += 1
        if count > 15:
            print("下载失败")


# urlretrieve()的回调函数，显示当前的下载进度
# a为已经下载的数据块
# b为数据块大小
# c为远程文件的大小
global myper

def jindu(a, b, c):
    if not a:
        print(a)
    if c < 0:
        print("要下载的文件大小为0")
    else:
        global myper, allcount
        per = 100 * a * b / c

        if per > 100:
            per = 100
        myper = per
        # print("当前下载进度为：" + '%.2f%%' % per)
    if per == 100:

        allcount +=1
        downloaded.set(str(allcount) + '下载完成！')
        return True

#
#
# 读取所有数据到groups
def get_huaban_beauty(pid):
    if (GPATH):
        if (os.path.exists(GPATH) == False):
            os.mkdir(GPATH)
    else:
        action.configure(state='normal')
        WIN.update()
        print('没有设置目录')
        return

    if pid is None or pid == '':
        action.configure(state='normal')
        WIN.update()
        # print u'none id'
        return
    pin_id = ''
    board_id = pid
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
    try:
        i_headers = {
            "User-Agent": "Mozilla/5.0 (WINdows NT 6.1; rv:2.0.1)Gecko/20100101 Firefox/4.0.1",
            "Connection": "keep-alive",
            "Host": "huaban.com",
            "Accept": "application/json"
        }
        req = urllib.request.Request(url, headers=i_headers)
        html = urllib.request.urlopen(req).read().decode("utf-8")
        reg = re.compile(
            '"pin_id":(.*?),.+?"file_id":(.*?),.+?"file":\{.+?"key":(.*?),.+?"type":"image\/(.*?)"', re.S)
        groups = re.findall(reg, html)
        firstid = groups[0][0][1:-3]
    except TypeError:
        print('地址错误')
    # print len(text_read('beauty/'+board_id+'/1.txt'))
    txtid = text_read(GPATH + '/' + board_id + '/1.txt')
    if len(text_read(GPATH + '/' + board_id + '/1.txt')) > 0:
        if txtid[len(txtid) - 1] == firstid:
            changelabel('没有新的图片')
            # print 'no refresh'
            return
        else:
            test_text = [firstid]
            text_save(test_text, GPATH + '/' + board_id + '/1.txt')
    test_text = [firstid]
    text_save(test_text, GPATH + '/' + board_id + '/1.txt')
    while board_id != None:
        # url = 'http://huaban.com/boards/31435061/?max=' + str(pin_id) + '&limit=' + str(limit) + '&wfl=1'
        url = 'http://huaban.com/boards/' + board_id + \
              '/?max=' + maxid + '&limit=' + str(limit) + '&wfl=1'
        try:
            i_headers = {
                "User-Agent": "Mozilla/5.0 (WINdows NT 6.1; rv:2.0.1)Gecko/20100101 Firefox/4.0.1",
                "Connection": "keep-alive",
                "Host": "huaban.com",
                "Accept": "application/json"
            }
            req = urllib.request.Request(url, headers=i_headers)
            html = urllib.request.urlopen(req).read().decode("utf-8")
            # print (html)
            # reg = re.compile('"pin_id":(.*?),.+?"file":{"farm":"farm1", "bucket":"hbimg",.+?"key":"(.*?)",.+?"type":"image/(.*?)"', re.S)
            reg = re.compile(
                '"pin_id":(.*?),.+?"file_id":(.*?),.+?"file":\{.+?"key":(.*?),.+?"type":"image\/(.*?)"',
                re.S)
            groups = re.findall(reg, html)

            if len(groups) <= 0:
                # changelabel('下载完成')
                action.configure(text=name.get() + '下载完成！')  # 设置button显示的内容
                action.configure(state='normal')
                WIN.update()
                # downloaded.set('图片下载完毕！')
                # print ('图片下载完毕！') # 图片下载完毕
                return
            maxid = groups[len(groups) - 1][0]
            if nowid == maxid:
                return
            else:
                nowid = maxid
            #     groups 全部匹配完毕可以开始下载数据
            for att in groups:
                pin_id = att[0][1:-3]
                att_url = att[2][1:-1]
                img_type = att[3]
                img_url = 'http://img.hb.aicdn.com/' + att_url
                # print txtid[len(txtid) - 1]
                if len(txtid) > 0:
                    if pin_id == txtid[len(txtid) - 1]:
                        changelabel('结束')
                        return
                # urllib.request.urlretrieve(img_url, GPATH + '/' + board_id + '/' + att_url + '.' + img_type, callbackfunc)
                # th = threading.Thread(target=urllib.request.urlretrieve,
                #                       args=(img_url, GPATH + '/' + board_id + '/' + att_url + '.' + img_type, jindu,))
                # th.setDaemon(True)  # 守护线程
                # th.start()

                # auto_down(img_url, GPATH + '/' + board_id + '/' + att_url + '.' + img_type)
                if urllib.request.urlretrieve(img_url, GPATH + '/' + board_id + '/' + att_url + '.' + img_type):
                    global downloadedCount
                    downloadedCount += 1
                    print('下载了：'+str(downloadedCount))
                    global downloaded
                    downloaded.set('下载了：' + str(downloadedCount))
                    global WIN
                    WIN.update()
                    print (img_url + ' 下载成功!')
                else:
                    print (img_url + '.' + img_type + ' save failed')
        except TypeError:
            print(' error occurs')

# GUI界面开始
global WIN
WIN = tk.Tk()
WIN.title("花瓣画板图片下载")  # 添加标题
# FRAME = FRAME(WIN, width=200,height = 500)
#
# FRAME.pack()
# FRAME.pack_propagate(0) # 使组件大小不变，此时width才起作用
FRAME = LabelFrame(WIN, text="花瓣画板ID", width=2000, fg='darkgray')  # 信息区
FRAME.pack()
FRAME.grid(row=1, column=0, sticky=N + S, padx=100, pady=100)

FRAME.propagate(0)  # 使组件大小不变，此时width才起作用

downloaded = StringVar()
downloaded.set('')


def clickme():
    """   # 当acction被点击时,该函数则生效"""
    action.configure(text=name.get() + '下载中，不要多次点击！')  # 设置button显示的内容
    action.configure(state='disabled')
    WIN.update()
    get_huaban_beauty(name.get().strip())
    print(groups)


def clickme1():
    """   # 当选择目录acction被点击时,该函数则生效"""
    global GPATH
    GPATH = ''
    path = askdirectory()
    if path:
        GPATH = path
        nameEntered1.delete(0, END)
        nameEntered1.insert(0, GPATH)


def changelabel(labelname):
    """改变标题"""
    action.configure(text=name.get() + labelname)  # 设置button显示的内容
    action.configure(state='normal')
    WIN.update()


# 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
action = ttk.Button(FRAME, text=iid, command=clickme)
action.grid(column=1, row=1)

# 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
action1 = ttk.Button(FRAME, text='选择目录', command=clickme1)
action1.grid(column=1, row=2)

ttk.Label(FRAME, text="输入画板ID:").grid(column=0, row=0)

# StringVar是Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符；不过一般用在按钮button上。改变StringVar，按钮上的文字也随之改变。
name = tk.StringVar()
# 创建一个文本框，定义长度为12个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickme调用
nameEntered = ttk.Entry(FRAME, width=50, textvariable=name)
nameEntered.grid(column=0, row=1)
# 创建一个文本框，定义长度为12个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickme调用
nameEntered1 = ttk.Entry(FRAME, width=50)
nameEntered1.grid(column=0, row=2)

ttk.Label(FRAME, textvariable=downloaded).grid(column=0, row=3)
WIN.mainloop()  # 当调用mainloop()时,窗口才会显示出来

# mainRun()
