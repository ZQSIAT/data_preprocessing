# url管理器
# -*- coding: utf-8 -*-
import os


class findFileNames(object):
    def __init__(self):
        self.fileNames = []

    def file_name(self,path):
        for root in os.listdir(path):
            self.fileNames.append(root+",")

        with open("E:\\重命名\\names.txt",'w') as f:
            f.writelines(self.fileNames)


if __name__ == "__main__":
    my_start = findFileNames()
    file_dir1 = "E:\\标签程序\\temp"
    my_start.file_name(file_dir1)

