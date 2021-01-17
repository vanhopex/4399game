# -*- coding: utf-8 -*-

'''
@Time    : 2021/1/7 23:13
@Author  : Wanhao Zhang
@Contact : 1809721229@qq.com 
@FileName: preparation.py
@Software: PyCharm
 
'''
from time import sleep

from PIL import Image, ImageGrab

import win32gui

# 找打句柄

# 宠物连连看经典版2小游戏,在线玩,4399小游戏 - 360安全浏览器
handle = win32gui.FindWindow(0, '宠物连连看经典版2小游戏,在线玩,4399小游戏 - 360安全浏览器 10.0')
# handle = win32gui.FindWindow(0, '爷的文件群')
if not handle:
    print('没找到句柄')
    exit()
win32gui.SetForegroundWindow(handle)


sleep(3)
img_grab = ImageGrab.grab()
img_grab.save('img_grab.jpg')
#
# img = Image.open('test.jpg')
box = (399, 305, 1247, 873)
region = img_grab.crop(box)
region.show()
region.save('newImg.jpg')
