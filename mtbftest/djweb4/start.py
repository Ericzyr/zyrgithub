#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import shutil
import time
import os
now = time.strftime("%Y%m%d_%H%M", time.localtime())
os.system('wget http://localhost:8000/child' + ".html")  # 这个是用打开一个django服务文件html文件生成一下html文件
for i in range(2):  # 用这个for方法是打开生成的html文件并对读取查找替换文件
    html = open("child.html", 'r+', encoding='utf-8')
    if i == 0:
        htmlcount = html.read()
        newhtml = htmlcount.replace('href="', 'href="/')     # html文件并对读取查找替换文件
    if i == 1:
        html.write(newhtml)
    html.close()
locat_path = os.popen('pwd').read()
source = locat_path.rsplit()[0] + "/child" + ".html"
target = os.path.dirname(os.getcwd()) + "/htmlFolder/" + now + ".html"
shutil.move(source, target)  # 文件mv移动
