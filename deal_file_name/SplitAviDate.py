# -*- coding: utf-8 -*-
'''
This python file is split the avi files to small files.

'''

import os
import time
import numpy as np
from PIL import Image
import pickle
from multiprocessing import Pool


def GetVideoList(a):
    FilesList = []
    FilesDir = os.listdir(a)
    FilesDir.sort()
    for i,ICount in enumerate(FilesDir):
        FilesList.append(a + ICount)
        pass
    return FilesList
    pass

def CompressFiles(a):
    Src = a
    Dst = Src.replace("SegmentationVideo", "CompressedVideo")
    if (os.path.exists(Dst)):
        print("{:s} already compressed~~~~!!!!!!!!!!!~~~~".format(Src))
        pass
    else:
        cmd_name = "ffmpeg -y -i {:s} -s 640x360 -b 4096000 {:s} -hide_banner".format(Src, Dst)
        os.system(cmd_name)
        print("{:s} has done.".format(Src))
        pass
    pass
    # for i,ICount in enumerate(a):
    # raise RuntimeError
    # pass
def IntraCoding(DS):
    DS[0].sort()
    for i,ICount in enumerate(DS[0]):
        VideoFils = os.listdir(ICount)
        VideoFils.sort()
        for j,JCount in enumerate(VideoFils):
            SrcDir = ICount + "/" + JCount
            DstDir = ICount + "/" + JCount.replace("record","record_key_frame")
            if (os.path.exists(DstDir)):
                print("{:s} has turned~~~!!!~~".format(JCount))
                pass
            else:
                IntraCodingCmd = "ffmpeg -y -i {:s} -strict -2  -qscale 0 -intra {:s}".format(SrcDir,DstDir)
                os.system(IntraCodingCmd)
                print("{:s} has turned to intra conding ~~!!!~~~".format(JCount))
                pass
            if (os.path.exists(SrcDir)):
                Dir_Delete = ICount.replace("/", "\\") + "\\" + JCount
                Cmd_Delete_bin = "del " + Dir_Delete
                os.system(Cmd_Delete_bin)
                print("{:s} has deleted~~~!!!~~".format(JCount))
                pass
            pass
            # raise RuntimeError
        print("{:s} has done~~~!!!~~".format(ICount))
        # break
        pass
    pass

def SplitAviDate(DS,LS):
    LS[0].sort()
    LS[1].sort()
    DS[0].sort()
    DS[1].sort()
    for ii, ICount in enumerate(LS[1]):
        txt_list = os.listdir(ICount)
        txt_list = list(filter(lambda x: x.endswith('.txt'), txt_list))
        txt_list.sort()
        for j,jCount in enumerate(txt_list):
            TxtDir = ICount + "/" + jCount
            with open(TxtDir) as lf:
                Lines = lf.readlines()[:-1]
                LinesNumber = len(Lines)
                if (LinesNumber % 2 == 0):
                    SegmentationNumber = int(LinesNumber / 2 - 1)
                    for i in range(SegmentationNumber):
                        StartTime = TimeSubtraction(Lines[2 * i + 1].split(" *# ", 2)[1], Lines[0].split(" ", 2)[1])
                        DurationTime = TimeSubtraction(Lines[2*(i+1)].split(" #* ", 2)[1], Lines[2 * i + 1].split(" *# ", 2)[1])
                        if (DurationTime[1] == "no"):
                            print("{:s} {:s}Time is short~~~!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!~~~~ ".format(Lines[2 * i + 1].split(" *# ", 2)[0],TxtDir))
                            pass
                        VideoDir = ICount.replace("LABEL","HIKVISION") + jCount.replace(".txt","/")
                        VideoList = os.listdir(VideoDir)
                        for k,KCount in enumerate(VideoList):
                            SubjectNumber = SubjectList.index(ICount.split("/", 5)[4])
                            CameraNumber = int(KCount.split("_")[0][11:]) - 1
                            ActionNumber = ActionList.index(Lines[2 * i + 1].split(" *# ", 2)[0])
                            # print(Lines[2 * i + 1].split(" *# ", 2)[0])
                            # raise RuntimeError
                            TimeNumber = int(jCount.replace(".txt","")[-2:]) - 1
                            DstSmallVideoDir = "{:s}s{:03d}_c{:02d}_a{:02d}_t{:02d}.mp4".format(SegmentationDir,SubjectNumber,CameraNumber,ActionNumber,TimeNumber)
                            SrcVideoDir = VideoDir + KCount
                            FfmpegcCmd = "ffmpeg -y -ss {:s} -t {:s} -i {:s} -vcodec copy -acodec copy {:s} -hide_banner".format(StartTime[0], DurationTime[0], SrcVideoDir, DstSmallVideoDir)
                            # print(FfmpegcCmd)
                            # raise RuntimeError
                            if (os.path.exists(DstSmallVideoDir)):
                                print("{:s} already exists~~~".format(DstSmallVideoDir))
                                pass
                            else:
                                os.system(FfmpegcCmd)
                                print("{:s} has done~~~!!!~~~".format(DstSmallVideoDir))
                                pass
                            pass
                        pass
                    pass
                else:
                    print("{:s} was broken~~!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!~~".format(TxtDir))
                    pass
                pass
            # raise RuntimeError
            pass
        pass
    pass

def TimeSubtraction(End, Start):

    StartTotalTime = (int(Start.split("-")[0])*3600 + int(Start.split("-")[1])*60 + int(Start.split("-")[2]))*1000 + int(Start.split("-")[3])
    EndTotalTime = (int(End.split("-")[0])*3600 + int(End.split("-")[1])*60 + int(End.split("-")[2]))*1000 + int(End.split("-")[3])
    SubtractionTime = EndTotalTime - StartTotalTime
    milliseconds = int(SubtractionTime % 1000)
    Minutes, Seconds = divmod(int((SubtractionTime - milliseconds) / 1000), 60)
    Hours, Minutes = divmod(Minutes, 60)
    Duration = "{:02d}:{:02d}:{:02d}.{:03d}".format(Hours, Minutes, Seconds, milliseconds)

    if (SubtractionTime > 999):
        return Duration,"yes"
        pass
    else:
        return Duration, "no"
        pass
    pass

def RenameFiles(a):
    a.sort()
    for i,ICount in enumerate(a):
        LongSequenceList = os.listdir(ICount)
        LongSequenceList.sort()
        if (len(LongSequenceList[0]) < 9):
            print("The {:s} has done~~~~!!!~~~~".format(ICount))
            continue
            pass
        elif (len(LongSequenceList) == 24):
            for j,JCount in enumerate(LongSequenceList):
                SrcDir = ICount + JCount
                if (JCount[:3] == "bla"):
                    NewName = JCount.replace(JCount[5:],"t0{:d}".format(j%3 + 1))
                    pass
                else:
                    NewName = JCount.replace(JCount[4:], "t0{:d}".format(j % 3 + 1))
                    pass
                DstDir = ICount + NewName
                os.rename(SrcDir,DstDir)
                pass
            pass
        else:
            print("The length of {:s} is not 24, or has done~~~~!!!~~~~".format(ICount))
            continue
            pass
        pass
        # raise RuntimeError
    pass

def RenameLabelFiles(a):
    a.sort()
    for i,ICount in enumerate(a):
        LongSequenceList = os.listdir(ICount)

        LongSequenceList.sort()
        if (len(LongSequenceList[0]) < 13):
            print("The {:s} has done~~~~!!!~~~~".format(ICount))
            continue
            pass
        elif (len(LongSequenceList) == 24):
            for j,JCount in enumerate(LongSequenceList):
                SrcDir = ICount + JCount
                if (JCount[:3] == "bla"):
                    NewName = JCount.replace(JCount[5:],"t0{:d}".format(j%3 + 1))
                    pass
                else:
                    NewName = JCount.replace(JCount[4:], "t0{:d}".format(j % 3 + 1))
                    pass
                DstDir = ICount + NewName + ".txt"
                os.rename(SrcDir,DstDir)
                print("The {:s} has renamed~~~~!!!~~~~".format(ICount))
                pass
            pass
        else:
            print("The length of {:s} is not 24, or has done~~~~!!!~~~~".format(ICount))
            continue
            pass
        pass
        # raise RuntimeError
    pass
# 获得文件列表
def GetPictureList(a = "F:/DATASET/"):
    ActioLiat = []
    SubjectList = []
    SubjectDirs = os.listdir(a)
    for i,ICount in enumerate(SubjectDirs):
        LongSequenceList = os.listdir(a + ICount)
        SubjectList.append(a + ICount + "/")
        for j,JCount in enumerate(LongSequenceList):
            ActioLiat.append(a + ICount + "/" + JCount)
            pass
        pass
        #break
    return ActioLiat,SubjectList
    pass

if __name__ == "__main__":

    DataSourceDir = "D:/0000DATA/DATASET_TEST/HIKVISION/"
    LabelDataDir = "D:/0000DATA/DATASET_TEST/LABEL/"
    SegmentationDir = "D:/0000DATA/DATASET_TEST/SegmentationVideo/"
    DataSourceSequence = GetPictureList(DataSourceDir)
    LabelDataSequence = GetPictureList(LabelDataDir)
    SegVideoList = GetVideoList(SegmentationDir)
    global SubjectList, ActionList
    SubjectList = os.listdir(DataSourceDir)
    ActionList = ["wear glasses", "caps", "salute", "combs", "throw things", "play mobile phone", "self-timer",
                  "Reading", "Signature", "typing", "calling", "turn around", "fast walk", "walk", "jogging",
                  "Pick up thing", "watch watch", "cough", "drink water", "eat things", "smoke", "wipe sweat", "thrush",
                  "Run", "jumps", "jump ropes", "leapfrogs", "Underarm", "falls", "back lying down", "Painful collapse",
                  "Pull the sword", "archery", "pull guns", "remove the baseball bat", "Basketball dribbling",
                  "basketball shooting", "Basketball ball control", "Table tennis ball", "table tennis serve",
                  "holding the ball", "backhand catching the ball", "Badminton ball", "badminton serve",
                  "badminton smash", "step badminton catch", "Guitar Sweeping", "Folk Fingers", "Blow bamboo flute",
                  "blow the harmonica", "take the microphone", "blow the clarinet", "playing piano",
                  "Basketball dribble attack and defense", "basketball air pass", "football pass", "Handshake",
                  "high-five", "handover things", "toast", "Embrace", "Wrestling", "Fighting", "Duel with sword",
                  "01-jump", "01-happy_jump", "01-crouch", "01-sad_squat", "01-throw", "01-angry_throw", "01-retreat",
                  "01-surprise_retreat", "01-back", "01-fear_back", "01-turn", "01-disgust_turn"]

    # raise RuntimeError
    print("Start processing...")
    starttime = time.time()
    print("#" * 120)

    # CompressFiles(SegVideoList)
    # IntraCoding(DataSourceSequence)
    # SplitAviDate(DataSourceSequence,LabelDataSequence)
    # RenameLabelFiles(LabelDataSequence[1])
    # processing by pool map
    p = Pool(6)
    res1 = p.map(CompressFiles, SegVideoList)

    endtime = time.time()
    print("#" * 120)
    print("Finished! Time elapse: {:.2f} minutes.".format((endtime - starttime) / 60.0))

    pass

