# 重命名
# 取出原标签的名字，用正则匹配出编号
# -*- coding: utf-8 -*-
import os


class renameLabel(object):
    def __init__(self):
        self.fileNames = []
        self.newNames = []
        self.number = 0
        self.o = 0

    def rename(self,path):
        for i in os.listdir(path):
            self.number = int(i[1:2]) * 100 + int(i[2:3]) * 10 + int(i[3:4])
            if (self.number <= 66):
                self.o = 1
            elif (self.number >= 91):
                self.o = 3
            else:
                self.o = 2
            oNumber = "O00" + str(self.o)
            newName = oNumber + i
            os.rename(os.path.join(path, i), os.path.join(path, newName))



if __name__ == "__main__":
    my_start = renameLabel()
    file_dir1 = "E:\\标签程序\\重命名后的输出标签"
    my_start.rename(file_dir1)

