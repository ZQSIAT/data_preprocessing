# url管理器
# -*- coding: utf-8 -*-
import os


class findRepeatFiles(object):
    def __init__(self):
        self.fileNames = []
        self.count = 0

    def file_name(self,path,path1):
        for root in os.listdir(path):
            self.fileNames.append(root)

        for i in self.fileNames:
            newPath = path1 + "\\" + i + ".txt"
            if(os.path.exists(newPath) == True):
                self.count = self.count+1
                print("我重复的文件是")
                print(i)
            else:
                open(newPath, 'w')
        print(self.count)

if __name__ == "__main__":
    my_start = findRepeatFiles()
    file_dir1 = "E:\\标签程序\\temp"
    file_dir2 = "E:\\标签程序\\newtxts"
    my_start.file_name(file_dir1,file_dir2)

