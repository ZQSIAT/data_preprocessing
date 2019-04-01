# This code is designed for find bad skeleton files, and delete it.

import shutil as st
import os
import time
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



if __name__ == "__main__":
    # find_ntu_skeleton_bad_data_and_delete_it()
    # source_files_1 = "E:/DATASET_COPY_B/KINECTDATA_B/KINECT04/"
    # source_files_2 = "J:/DATASET_k4/"
    # source_files_d = "//Zqsiat/cas_mhad/DATASETBACKUP/KINECT03/"
    # s1 = os.listdir(source_files_1)
    # s2 = os.listdir(source_files_2)
    # d = os.listdir("//Zqsiat/cas_mhad/DATASETBACKUP/KINECT03/")
    # print(len(d))
    # s = s1 + s2
    #
    # print(len(s))
    # for i,ICount in enumerate(d):
    #     if (len(os.listdir(source_files_d+ICount)) != 24):
    #         print("{:s}   ERROR!!!!!!".format(source_files_d+ICount))
    #         print("#" * 120)
    #         pass
    #     pass
    # retE = [i for i in s1 if i in s2]
    # print(retE)
    # print(len(retE))
    all_list = []
    subject_1_91 = "//172.20.15.56/cas_mhad/DATASET_BACKUP/HIKVISION/1-91_HIKVISION/"
    subject_92_276 = "//172.20.15.56/cas_mhad/DATASET_BACKUP/HIKVISION/92-276_HIKVISION/"
    list1_91 = os.listdir(subject_1_91)
    list1_185 = os.listdir(subject_92_276)
    all_list = list1_91+list1_185
    all_list.sort()
    print(all_list)
    print(len(all_list))
    all_peple_list = open('{:s}_all_peple_list.txt'.format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())), 'w')
    all_peple_list.write(str(all_list))
    all_peple_list.close()
    pass