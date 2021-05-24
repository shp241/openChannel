import math
import os

import cv2
import numpy as np
import matplotlib.pyplot as plt

debug = False
deplot = False


# 色阶转换
def white_black_level_pretreatment(img, Shadow, Highlight):
    if Highlight > 255:
        Highlight = 255
    if Shadow < 0:
        Shadow = 0
    if Shadow >= Highlight:
        Shadow = Highlight - 2
    # 转类型
    img = np.array(img, dtype=int)
    # 计算白场黑场离差
    Diff = Highlight - Shadow
    # 计算系数
    coe = 255.0 / Diff
    rgbDiff = img - Shadow
    rgbDiff = np.maximum(rgbDiff, 0)
    img = rgbDiff * coe
    # 四舍五入到整数
    img = np.around(img, 0)
    return img


def adjust_image(d, deform, start, rule, nr):
    # 加载图片，获取宽高
    img = cv2.imread(d, 1)
    imgInfo = img.shape
    height = imgInfo[0]
    width = imgInfo[1]
    # 拉伸坐标
    to = np.float32([(0, 0),
                     (width - 1, 0),
                     (0, height - 1),
                     (width - 1, height - 1)])
    # 扭曲形变
    dst = cv2.getPerspectiveTransform(deform, to)
    img = cv2.warpPerspective(img, dst, (width, height))
    if debug:
        cv2.imwrite("1.jpg", img)
    # 截取矩形进行识别
    img = img[start[1]:start[1] + rule * nr, start[0]:start[0] + rule]
    # 设置灰度
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 调整色阶
    img = white_black_level_pretreatment(img, 85, 170)
    cv2.imwrite(d.replace("image", "make"), img)
    return img


def get_deep(img, nr):
    # 获取大格平均数
    img15 = cv2.resize(img, (1, nr))
    img15.resize(nr)
    if debug:
        cv2.imwrite("3.jpg", img15)
    # 对平均数求导获取大格导数最大值
    dx15 = img15 - np.append(img15[1:], img15[-1])
    if deplot:
        plt.plot(dx15)
        plt.show()
    n = np.argmax(dx15) + 1
    # 大格周围+-0.5进行小格取值
    img150 = cv2.resize(img, (1, nr * 10))
    img150.resize(nr * 10)
    if 0 < n < nr:
        img150 = img150[n * 10 - 5:n * 10 + 5]
    elif n == 0:
        p = img150[0]
        img150 = np.append([p, p, p, p, p], img150[0:n * 10 + 5])
    elif n == nr:
        p = img150[-1]
        img150 = np.append(img150[n * 10 - 5:], [p, p, p, p, p])
    if debug:
        cv2.imwrite("4.jpg", img150)
    # 对小格求导获取小格导数最大值
    dx150 = img150 - np.append(img150[1:], img150[-1])
    nd = np.argmax(dx150) + 1
    if deplot:
        plt.plot(dx150)
        plt.show()
    return nr - n + (5 - nd) * 0.1


# 矩形四点
ori = {r"image\1": np.float32([(450, 513),
                               (3590, 435),
                               (989, 1779),
                               (3119, 1738)]),
       r"image\2": np.float32([(844, 599),
                               (3347, 798),
                               (780, 2270),
                               (3261, 2333)]),
       r"image\3": np.float32([(197, 409),
                               (3613, 369),
                               (868, 1922),
                               (3020, 1924)]),
       }

# 水位检测起始点
x = {r"image\1": (2200, 705),
     r"image\2": (2530, 750),
     r"image\3": (1340, 615),
     }
# 图像水位单位像素高度
a = {r"image\1": 153,
     r"image\2": 150,
     r"image\3": 149,
     }
# 水位尺度最大格数
k = {r"image\1": 15,
     r"image\2": 15,
     r"image\3": 15,
     }

# img = adjust_image(r"image\2\2_9.0.jpg", ori[r"image\2"], x[r"image\2"], a[r"image\2"], k[r"image\2"])
# print(get_deep(img, k[r"image\2"]))
# debug = True
for root, dirs, files in os.walk(r"image"):
    for f in files:
        d = root + '\\' + f
        print(d)
        img = adjust_image(d, ori[root], x[root], a[root], k[root])
        print(get_deep(img, k[root]))
