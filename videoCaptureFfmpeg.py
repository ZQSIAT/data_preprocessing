# -*- coding: UTF-8 -*-
import os
import subprocess
import time
from multiprocessing.pool import Pool

import numpy as np

class videoCapture:
    #def __init__(self):
    def changeFrameToTime(self,frame):
        frame = float(frame)
        a = frame/25.0
        seconds = float('%.3f' % a)
        print("seconds", seconds)
        milliseconds = int(str(seconds)[2:])
        #print("milliseconds",milliseconds)
        seconds = int(frame/25.0)
        Minutes, Seconds = divmod(seconds, 60)
        Hours, Minutes = divmod(Minutes, 60)
        time = "{:02d}:{:02d}:{:02d}.{:0<2d}".format(Hours, Minutes, Seconds, milliseconds)
        print(time)
        return time

    def getFilePath(self,pathIn):
        filePathList = []
        dirs = []
        # pathIn: \\10.10.1.49\cas_mhad\Preprocessing_Test\DataSet1\RGB_HIKVISION
        # pathIn: E:\videosample
        for file in os.listdir(pathIn):
            if (file[-5:-4] == "5"):
                #print(file)
                filepath = os.path.join(pathIn, file)
                filePathList.append(filepath)
        return filePathList

    def Capture(self, filePath):
        # filePath: \\10.10.1.49\cas_mhad\Preprocessing_Test\DataSet1\RGB_HIKVISION\O001P009C001T001S005.mp4
        # pathOut: E:\视频分割\1-91 a05
        # filePathOut: E:\视频分割\1-91 a05\O001P009C001T001S005(A001).mp4
        #print(filePath)
        #fileName = filePath[-24:-4]
        fileName = filePath[-24:-4]
        fileOutName = '{}{}'.format(fileName, "(A001)")

        #print(fileOutName)
        # 找起始帧和结束帧
        framePathIn = "E:\标签程序\现在输出标签"
        fileName1 = '{}{}{}'.format(fileName[4:8], fileName[-8:], ".txt")
        framePath = '{}\{}'.format(framePathIn, fileName1)

        f1 = open(framePath, "r")
        lines = f1.readlines()
        arrTemp = lines[0].split(',')
        start = self.changeFrameToTime(arrTemp[1])
        print("start",start)
        durationFrame = int(arrTemp[2]) - int(arrTemp[1])
        duration = self.changeFrameToTime(durationFrame)
        print("duration", duration)
        f1.close()

        pathOut = r"E:\videocapture\1-91-a05"
        filePathOut = '{}\{}{}'.format(pathOut, fileOutName, ".avi")

        FfmpegcCmd = "ffmpeg -i {:s} -vcodec copy -acodec copy -ss {:s} -t {:s} {:s}".format(
            filePath, start, duration , filePathOut)
        #FfmpegcCmd = "ffmpeg -y -ss {:s} -t {:s} -i {:s} -vcodec copy -acodec copy {:s} -hide_banner".format(
            #start, duration, filePath, filePathOut)

        print(FfmpegcCmd)
        if (os.path.exists(filePathOut)):
            print("{:s} already exists~~~".format(filePathOut))
            pass
        else:
            os.system(FfmpegcCmd)
            #print("{:s} has done~~~!!!~~~".format(filePathOut))
            pass


if __name__ == "__main__":
    pro = videoCapture()
    # pathIn：要处理的文件夹
    #pathIn = r"\\10.10.1.49\cas_mhad\Preprocessing_Test\DataSet1\RGB_HIKVISION"
    pathIn = r"E:\videosample"
    # pathOut：要处理的文件夹
    pathOut = r"E:\videocapture\1-91-a05"

    filePathList = pro.getFilePath(pathIn)
    print("一共有的数量是",filePathList.__len__())
    print('start ...')
    t1 = time.time() * 1000

    print('concurrent:4')  # 创建多个进程，并行执行
    pool = Pool(4)  # 创建拥有10个进程数量的进程池
    # testFL:要处理的数据列表，run：处理testFL列表中数据的函数
    pool.map(pro.Capture,filePathList)
    # pool.close()  # 关闭进程池，不再接受新的进程
    # pool.join()  # 主进程阻塞等待子进程的退出

    t2 = time.time() * 1000
    print('take time:' + str((t2 - t1) / 1000) + 's')
    print('end.')