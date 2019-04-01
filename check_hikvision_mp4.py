# This code is designed for find bad hikvision video mp4 files, and record somethings about it.

import shutil as st
import os
import time
from multiprocessing import Pool
# import cv2
# import pandas as pd
# import numpy as np
import random


def copy_wanted_sequence_hikvision(file_list,needed_replace_string="C_HIKVISION",wanted_action="a01"):
    for i,ICount in enumerate(file_list):
        src_path = ICount
        # print(ICount)
        # raise RuntimeError
        if "a01" in ICount and (wanted_action == "a01" or wanted_action == "all"):
            dst_a01_path = ICount.replace(needed_replace_string,"a01")
            if not os.path.exists(dst_a01_path) and os.path.exists(src_path):
                st.copytree(src_path,dst_a01_path)
                print("Have copyed \"{:s}\" .".format(ICount))
                pass
            pass

        if "a02" in ICount and (wanted_action == "a02" or wanted_action == "all"):
            dst_a02_path = ICount.replace(needed_replace_string, "a02")
            if not os.path.exists(dst_a02_path) and os.path.exists(src_path):
                st.copytree(src_path, dst_a02_path)
                print("Have copyed \"{:s}\" .".format(ICount))
                pass
            pass

        if "a03" in ICount and (wanted_action == "a03" or wanted_action == "all"):
            dst_a03_path = ICount.replace(needed_replace_string, "a03")
            if not os.path.exists(dst_a03_path) and os.path.exists(src_path):
                st.copytree(src_path, dst_a03_path)
                print("Have copyed \"{:s}\" .".format(ICount))
                pass
            pass
        if "a04" in ICount and (wanted_action == "a04" or wanted_action == "all"):
            dst_a04_path = ICount.replace(needed_replace_string, "a04")
            if not os.path.exists(dst_a04_path) and os.path.exists(src_path):
                st.copytree(src_path, dst_a04_path)
                print("Have copyed \"{:s}\" .".format(ICount))
                pass
            pass
        if "a05" in ICount and (wanted_action == "a05" or wanted_action == "all"):
            dst_a05_path = ICount.replace(needed_replace_string, "a05")
            if not os.path.exists(dst_a05_path) and os.path.exists(src_path):
                st.copytree(src_path, dst_a05_path)
                print("Have copyed \"{:s}\" .".format(ICount))
                pass
            pass
        if "a06" in ICount and (wanted_action == "a06" or wanted_action == "all"):
            dst_a06_path = ICount.replace(needed_replace_string, "a06")
            if not os.path.exists(dst_a06_path) and os.path.exists(src_path):
                st.copytree(src_path, dst_a06_path)
                pass
            pass
        if "a07" in ICount and (wanted_action == "a07" or wanted_action == "all"):
            dst_a07_path = ICount.replace(needed_replace_string, "a07")
            if not os.path.exists(dst_a07_path) and os.path.exists(src_path):
                st.copytree(src_path, dst_a07_path)
                print("Have copyed \"{:s}\" .".format(ICount))
                pass
            pass
        if "bla" in ICount and (wanted_action == "bla" or wanted_action == "all"):
            dst_bla_path = ICount.replace(needed_replace_string, "bla")
            if not os.path.exists(dst_bla_path) and os.path.exists(src_path):
                st.copytree(src_path, dst_bla_path)
                print("Have copyed \"{:s}\" .".format(ICount))
                pass
            pass
        else:
            print("\"{:s}\" NO COPY, ERROR!!!!!!!!!!!!!!!!!!!!!.".format(ICount))
            pass
        pass


def ffmpeg_read_mp4_frame_number(a):
    scales = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    a01 , a02 , a03 , a04 , bla , a05 , a06 , a07 = [[],[],[],[],[],[],[],[]]
    sum_number_mp4 = 0
    mean_sequence = np.zeros(8)
    median_sequence = np.zeros(8)
    video_path = ""
    for i, ICount in enumerate(a):
        action_name = ICount.split('/',4)[3][0:3]
        camera_list = os.listdir(ICount)
        # print(camera_list)
        sum_number_mp4 = sum_number_mp4 + 1
        if len(camera_list) > 0:
            video_path = ICount + camera_list[random.choice(range(len(camera_list)))]
            pass
        else:
            print("{:s} has error~~~~!!!!~~~~".format(video_path))
            pass
        # print(video_path)
        capture = cv2.VideoCapture(video_path)
        if capture.isOpened():
            FrameNumber = capture.get(7)
            duration = round(FrameNumber / 25)
            if action_name == "a01":
                a01.append(duration)
                # print(duration,"a01")
                pass
            elif action_name == "a02":
                a02.append(duration)
                # print(duration,"a02")
                pass
            elif action_name == "a03":
                a03.append(duration)
                pass
            elif action_name == "a04":
                a04.append(duration)
                pass
            elif action_name == "a05":
                a05.append(duration)
                pass
            elif action_name == "a06":
                a06.append(duration)
                pass
            elif action_name == "a07":
                a07.append(duration)
                pass
            elif action_name == "bla":
                bla.append(duration)
                pass
            else:
                print("En ao {:s} need you deal~~~~~~~~".format(video_path))
                pass
            pass
        else:
            print("{:s} has broken~~~~!!!!~~~~".format(video_path))
            pass
        # break
        # raise RuntimeError
        pass
    pass

    mean_sequence[0] = np.mean(np.array(a01))
    mean_sequence[1] = np.mean(np.array(a02))
    mean_sequence[2] = np.mean(np.array(a03))
    mean_sequence[3] = np.mean(np.array(a04))
    mean_sequence[4] = np.mean(np.array(a05))
    mean_sequence[5] = np.mean(np.array(a06))
    mean_sequence[6] = np.mean(np.array(a07))
    mean_sequence[7] = np.mean(np.array(bla))

    median_sequence[0] = np.median(np.array(a01))
    median_sequence[1] = np.median(np.array(a02))
    median_sequence[2] = np.median(np.array(a03))
    median_sequence[3] = np.median(np.array(a04))
    median_sequence[4] = np.median(np.array(a05))
    median_sequence[5] = np.median(np.array(a06))
    median_sequence[6] = np.median(np.array(a07))
    median_sequence[7] = np.median(np.array(bla))

    print("There are \"{:08d}\" mp4 files".format(sum_number_mp4))

    print("\"a01,a02,a03,a04,a05,a06,a07,bla\", Their mean are: \n", mean_sequence)
    print("\"a01,a02,a03,a04,a05,a06,a07,bla\", Their median are: \n", median_sequence)

    data_duration = [a01,a02,a03,a04,a05,a06,a07,bla]
    # print(data_duration)
    index_name = ['a01', 'a02', 'a03','a04', 'a05', 'a06', 'a07', 'bla']
    test = pd.DataFrame(index=index_name,data=data_duration)
    test.to_csv("92-276_data_duration_{:s}.csv".format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())), encoding='gbk')

    pass


def ffmpeg_convert_encode_way(ICount):
    # for i, ICount in enumerate(a):
    camera_list = os.listdir(ICount)
    # print(camera_list)
    for j, JCount in enumerate(camera_list):
        video_path = ICount + JCount
        dst_video_path = video_path.replace("HIKVISION","C_HIKVISION")
        if os.path.exists(ICount.replace("HIKVISION","C_HIKVISION")) == False:
            os.makedirs(ICount.replace("HIKVISION","C_HIKVISION"))
        # print(video_path)
        cmd_ffmpeg_convert_file = "ffmpeg -y -i {:s} -strict -2 -q:a 0 -intra -s 640x360 {:s}".format(video_path,dst_video_path)
        # print(os.system(cmd_ffmpeg_convert_file))
        if os.system(cmd_ffmpeg_convert_file) == 0:
            print("{:s} was converted good!".format(video_path))
            pass
        else:
            print("~~~ {:s} convert was error ~~~".format(video_path))
            pass
        # raise RuntimeError
        pass
    pass
    # pass

def find_ffmpeg_hikvision_mp4_broken(a):

    broken_mp4_subject = open('test {:s}_broken_mp4_subject.txt'.format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())), 'w')

    for i, ICount in enumerate(a):
        camera_list = os.listdir(ICount)
        # print(camera_list)
        for j, JCount in enumerate(camera_list):
            video_path = ICount + JCount
            # print(video_path)
            cmd_ffmpeg_check_file = "ffmpeg -v error -i {:s} -f null -".format(video_path)
            # os.system(cmd_ffmpeg_check_file)
            if os.system(cmd_ffmpeg_check_file) == 0:
                print("{:s} is good!".format(video_path))
                pass
            else:
                print("~~~ {:s} was broken ~~~".format(video_path))
                broken_mp4_subject.write(str(video_path) + " was broken ~~~~~!!!\n")
                pass
            # raise RuntimeError
            pass
        pass
    broken_mp4_subject.close()
    pass

def find_hikvision_data_number_error(a):

    error_mp4_subject = open('92-276 {:s}_error_mp4_subject.txt'.format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())), 'w')

    for i,ICount in enumerate(a):
        LongSequenceList = os.listdir(ICount)

        if len(LongSequenceList) != 21:
            print("!!!~~~~~ {:s} the number of sample is error ~~~~~!!!".format(ICount))
            error_mp4_subject.write(str(ICount) + " the number of sample is error ~~~~~!!!\n")
            pass
        else :
            print("{:s} the number of sample is right ！ ".format(ICount))

            pass
        for j, JCount in enumerate(LongSequenceList):
            camera_list = os.listdir(ICount + JCount)

            if len(camera_list) != 15:
                print("!!!~~~~~ {:s} the camera number of sequence is error ~~~~~!!!".format(ICount + JCount))
                error_mp4_subject.write(str(ICount + JCount) + " the camera number of sequence is error ~~~~~!!!\n")
                pass
            else:
                print("{:s} the camera number of sequence is right ！ ".format(ICount + JCount))

                pass
            pass
        pass
    error_mp4_subject.close()
    pass

def find_ntu_skeleton_bad_data_and_delete_it():
    skeleton_dir = 'F:/ntu_rgbd_skeletons/'
    txt_file = 'F:/bad_data_list.txt'
    with open(txt_file) as lf:
        for line in lf.readlines():
            label_line = line.strip('\n')
            delete_path = skeleton_dir + label_line + '.skeleton'
            if (os.path.exists(delete_path)):
                os.remove(delete_path)
                print("{:s} has deleted!!!".format(label_line))
                pass
            else:
                print("A enenenneenen~~~ {:s} does not existed!!!!!!!!!".format(label_line))
                pass
            pass
        lf.close()
        pass
    pass

# 获得文件列表
def GetPictureList(a = "F:/DATASET/"):
    ActionList = []
    SubjectList = []
    SubjectDirs = os.listdir(a)
    for i,ICount in enumerate(SubjectDirs):
        LongSequenceList = os.listdir(a + ICount)
        SubjectList.append(a + ICount + "/")
        for j,JCount in enumerate(LongSequenceList):
            ActionList.append(a + ICount + "/" + JCount + "/")
            pass
        pass
        #break
    return ActionList,SubjectList
    pass

def GetVideoList(a):
    FilesList = []
    FilesDir = os.listdir(a)
    FilesDir.sort()
    for i,ICount in enumerate(FilesDir):
        FilesList.append(a + ICount)
        pass
    return FilesList
    pass

if __name__ == "__main__":

    # read_time_path = "I:/92-276_C_HIKVISION/"
    read_time_path = "D:/92-276_C_HIKVISION/"
    FilesDir = GetPictureList(read_time_path)

    print("Start processing...")
    start_time = time.time()
    print("#" * 120)
    needed_replace_string = "92-276_C_HIKVISION"
    wanted_action = "a02"
    copy_wanted_sequence_hikvision(FilesDir[0],needed_replace_string,wanted_action)
    # ffmpeg_read_mp4_frame_number(FilesDir[0])

    end_time = time.time()
    print("#" * 120)
    print("Finished! Time elapse: {:.2f} minutes.".format((end_time - start_time) / 60.0))

    pass
