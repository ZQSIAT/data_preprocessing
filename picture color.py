import random
from PIL import Image, ImageOps
import numpy as np
import numbers
import cv2
import math
import os
from sklearn import preprocessing
import matplotlib.pyplot as plt

if __name__ == "__main__":
    temp_path = "F:/pycharm_preject/temp/"
    img = cv2.imread(temp_path + "berry.jpg")
    B, G, R = cv2.split(img)
    cv2.imshow("B", B)
    cv2.imshow("G", G)
    cv2.imshow("R", R)

    HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # RGB 转为 HSV
    H, S, V = cv2.split(HSV)  # 分离 HSV 三通道
    cv2.imshow("H", H)
    cv2.imshow("S", S)
    cv2.imshow("V", V)
    Lowerred0 = np.array([155, 43, 35])
    Upperred0 = np.array([180, 255, 255])
    mask1 = cv2.inRange(HSV, Lowerred0, Upperred0)
    Lowerred1 = np.array([0, 43, 35])
    Upperred1 = np.array([11, 255, 255])
    mask2 = cv2.inRange(HSV, Lowerred1, Upperred1)  # 将红色区域部分归为全白，其他区域归为全黑
    Apple = mask1 + mask2
    cv2.imshow("apple", Apple)
    cv2.waitKey(0)
    pass
