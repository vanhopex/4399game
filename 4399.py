# -*- coding: utf-8 -*-

'''
@Time    : 2021/1/7 21:58
@Author  : Wanhao Zhang
@Contact : 1809721229@qq.com 
@FileName: 4399.py
@Software: PyCharm
 
'''
import operator
import time
import win32gui
from PIL import ImageGrab
import numpy as np
from pymouse import PyMouse


class GameAssist:
    def __init__(self, wdname):
        self.num_matrix = []
        self.map_matrix = []

        self.width = 71
        self.base_x =  399
        self.base_y =  305

        self.click_time = 0
        self.mouse = PyMouse()
        # 获取窗口的句柄
        self.hwnd = win32gui.FindWindow(0, wdname)

        if self.hwnd == 0:
            print('no such hwnd')
            exit(1)
        # 将该窗口显示在最前面
        win32gui.SetForegroundWindow(self.hwnd)

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
        return num_matrix

    def get_direct_connected(self, x, y):
        # 同一行直接相连的点
        ans_list = []

        row =  x - 1
        while row >= 0:
           if self.map_matrix[row][y] == 0:
                ans_list.append([row, y])
           else:
                break
           row = row - 1

        row = x + 1
        while row < self.map_matrix.shape[0]:
            if self.map_matrix[row][y] == 0:
                ans_list.append([row, y])
            else:
                break
            row = row + 1

        col = y - 1
        while col >= 0:
            if self.map_matrix[x][col] == 0:
                ans_list.append([x, col])
            else:
                break
            col = col - 1

        col = y + 1
        while col < self.map_matrix.shape[1]:
            if self.map_matrix[x][col] == 0:
                ans_list.append([x, col])
            else:
                break
            col = col + 1

        return ans_list


    def is_row_connected(self, x, y1,  y2):
        if y1 > y2:
            tmp = y1
            y1  = y2
            y2  = tmp

        if y2 - y1 == 1:
            return True

        for i in range(y1+1, y2):
            if self.map_matrix[x][i] != 0:
                return False
        return True



    def is_col_connected(self, x1, x2, y):
        if x1 > x2:
            tmp = x1
            x1 = x2
            x2 = tmp

        if x2 - x1 == 1:
            return True

        for i in range(x1+1, x2):
            if self.map_matrix[i][y] != 0:
                return False

        return True



    def is_reachable(self, x1, y1, x2, y2):
        # 如果数字不相同，直接返回不可到达
        if self.map_matrix[x1][y1] != self.map_matrix[x2][y2]:
            return False

        list1  = self.get_direct_connected(x1, y1)
        list2  = self.get_direct_connected(x2, y2)


        for x1,y1 in list1:
            for x2,y2 in list2:

                # if x1 == x2 and y1 == y2:
                #     continue

                if x1 == x2:
                    if self.is_row_connected(x1, y1, y2):
                        return True

                elif y1 == y2:
                    if self.is_col_connected(x1, x2, y1):
                        return True
        return False


    def click_and_set0(self, x1, y1, x2, y2):
        # 确定需要点击的坐标的中心位置
        c_x1 =  int(self.base_x + (y1 - 1)*self.width + self.width/2)
        c_y1 =  int(self.base_y + (x1 - 1)*self.width + self.width/2)

        c_x2 =  int(self.base_x + (y2 - 1)*self.width + self.width/2)
        c_y2 =  int(self.base_y + (x2 - 1)*self.width + self.width/2)

        time.sleep(self.click_time)
        self.mouse.click(c_x1, c_y1)
        time.sleep(self.click_time)
        self.mouse.click(c_x2, c_y2)

        self.map_matrix[x1][y1] = 0
        self.map_matrix[x2][y2] = 0

    def scan_game(self):
        row_num = self.map_matrix.shape[0]
        col_num = self.map_matrix.shape[1]

        # self.click_and_set0(1,5,1,7)
        print(row_num)
        print(col_num)

        for i in range(1, row_num):
            for j in range(1, col_num):

                if self.map_matrix[i][j] == 0:
                    continue

                for l in range(1, row_num):
                    for k in range(1, col_num):

                        if i == l and j == k:
                            continue

                        if self.map_matrix[l][k] == 0:
                            continue

                        if self.is_reachable(i, j, l, k):
                            self.click_and_set0(i, j, l, k)
                            # print(self.map_matrix)
                            # break


    def start(self):
        # 获取图像矩阵
        animal_images = self.screen_grab()
        # 获取图标的数字矩阵
        self.num_matrix = self.image2num(animal_images)
        # 四周添加上0，做成地图矩阵
        self.map_matrix = np.zeros((self.num_matrix.shape[0] + 2, self.num_matrix.shape[1] + 2), dtype=np.uint32)
        # print(map_matrix.shape)
        self.map_matrix[1:9, 1:13] = self.num_matrix

        self.scan_game()
        self.scan_game() # 很不优雅地扫描两遍，数据量小，没有关系



if __name__ == "__main__":
    # 窗口句柄，使用windspy获取
    wdname = "宠物连连看经典版2小游戏,在线玩,4399小游戏 - 360安全浏览器 10.0"
    game_assist = GameAssist(wdname)
    game_assist.start()
