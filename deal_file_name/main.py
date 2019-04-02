# 程序入口
# -*- coding: utf-8 -*-
import os

from dealFileName import check_name


class Main(object):
    # 初始化所要用到的东西
    def __init__(self):
        self.check = check_name.CheckName()

    def checkCount(self, file_dir):
        self.check.file_name(file_dir)


if __name__ == "__main__":
    my_start = Main()
    file_dir1 = "E:\\标签程序\\temp"
    my_start.checkCount(file_dir1)


