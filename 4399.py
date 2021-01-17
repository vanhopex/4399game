# -*- coding: utf-8 -*-

'''
@Time    : 2021/1/7 21:58
@Author  : Wanhao Zhang
@Contact : 1809721229@qq.com 
@FileName: 4399.py
@Software: PyCharm
 
'''
import operator
import win32gui
from PIL import ImageGrab, Image
import numpy as np

class GameAssist:
    def __init__(self, wdname):

        # 获取窗口的句柄

        self.hwnd = win32gui.FindWindow(0, wdname)

        if self.hwnd == 0:
            print('no such hwnd')
            exit(1)
        # 将该窗口显示在最前面
        win32gui.SetForegroundWindow(self.hwnd)

        # 开始
        self.start()


    def screen_grab(self):
        # 获取整个屏幕截图
        image_grab = ImageGrab.grab()
        # 获取游戏中间动物图标截图
        box = (399, 305, 1247, 873)
        animals_iamge  = image_grab.crop(box)

        # 将每个动物图像分割，得到图像矩阵
        images_list = []
        offset = 71

        x0 = 0
        y0 = 0

        for i in range(8):
            images_row = []
            for j in range(12):
                # 小图标左上角的坐标
                x1 = x0 + j*offset
                y1 = y0 + i*offset
                # 小图标右下角的坐标
                x2 = x1 + offset
                y2 = y1 + offset
                # animals_iamge.crop((x1, y1, x2, y2)).show()
                # animals_iamge.crop((x1, y1, x2, y2)).save('animal'+str(i)+str(j)+".jpg")
                images_row.append(animals_iamge.crop((x1+5, y1+5, x2-5, y2-5)))

            images_list.append(images_row)

        return images_list


    def get_index(self, str01, threshold, str01_list):
        for i in range(len(str01_list)):
            diff = sum(map(operator.ne, str01, str01_list[i]))
            if diff < threshold:
                return i

        return -1

    def image2num(self, animal_images):

        # im = animal_images[0][0]
        # test = im.convert("L")
        # # print(type(test))
        # # print(test.getdata())
        # # im.show()
        # # print(im.size) # size is 71*71
        # # im_L = im.resize((20,20), Image.ANTIALIAS).convert("L")
        # # print(im_L)
        # # pixels = list(im_L.getdada())
        # # print(pixels)
        # #
        # im_L = im.convert("L")
        # pixels = list(im_L.getdata())
        # im_L.show()
        # # print(list(im.getdata()))
        # # print(list(im_L.getdata()))
        #
        # avg = sum(pixels) / len(pixels)
        #
        #
        # hash = "".join(map(lambda x: "1" if x > avg else "0", pixels))
        # print(type(hash))
        #
        # print(sum(map(operator.ne, hash, hash)))
        # # print(avg)

        # num_matrix = np.zeros((8,12), str)
        num_str01_matrix = []

        for i in range(8):
            num_row = []
            for j in range(12):
                im = animal_images[i][j]
                im_L = im.convert("L")
                # im_L.show()
                pixels = list(im_L.getdata())  # 每个点的像素值
                avg_pixel = sum(pixels) / len(pixels)
                str01 = "".join(map(lambda x: "1" if x > avg_pixel else "0", pixels))
                num_row.append(str01)

            num_str01_matrix.append(num_row)

        # print(sum(map(operator.ne, num_str01_matrix[0][9], num_str01_matrix[7][0])))
        # animal_images[0][9].show()
        # animal_images[7][0].show()

        for i in range(12):
            print("(0,"+ str(i) +")", end='')
            print(sum(map(operator.ne, num_str01_matrix[0][0], num_str01_matrix[0][i])))

        threshold = 800 # 低于这个阈值认为是同一种图片
        image_type_list = [] # 所有图标的类型
        num_matrix = np.zeros((8,12), dtype=np.uint32)  #创建一个全0矩阵
        # 将每个点的数字串转换成一个特定数字
        for i in range(8):
            for j in range(12):

                index = self.get_index(num_str01_matrix[i][j], threshold, image_type_list)

                if index < 0:
                    image_type_list.append(num_str01_matrix[i][j])
                    num_matrix[i][j] = len(image_type_list)
                else:
                    num_matrix[i][j] = index+1
        # print(num_matrix)
        # print(image_type_list)
        return num_matrix



    def start(self):
        # 获取图像矩阵
        animal_images = self.screen_grab()
        # 获取图标的数字矩阵
        num_matrix = self.image2num(animal_images)
        # 四周添加上0，做成地图矩阵
        map_matrix = np.zeros((num_matrix.shape[0] + 2, num_matrix.shape[1] + 2), dtype=np.uint32)
        # print(map_matrix.shape)
        map_matrix[1:9, 1:13] = num_matrix
        print(map_matrix)


if __name__ == "__main__":
    # 窗口句柄，使用windspy获取
    wdname = "宠物连连看经典版2小游戏,在线玩,4399小游戏 - 360安全浏览器 10.0"
    game_assist = GameAssist(wdname)
    # game_assist.start()